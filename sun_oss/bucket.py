# -*- coding: utf-8 -*-

import os
import hashlib
import functools

from PIL import Image, ExifTags

import oss2
import qiniu
import qcloud_cos

from .exceptions import qiniu_error_handler
from .utils import qiniu_result_handler, qiniu_bool_result_handler, aliyun_list_result_handler, qiniu_list_result_handler
from .utils import normalize_endpoint


class _BucketBase(object):

    _IMAGES_ALLOWED = ('.gif', '.jpg', '.jpeg', '.png', '.bmp', '.webp')

    _endpoints = {}
    _cdn_endpoints = {}

    def __init__(self, access_key_id, access_key_secret, bucket_name, endpoint, cdn_endpoint):
        self.id = access_key_id.strip()
        self.secret = access_key_secret.strip()

        self._add_endpoint(bucket_name, endpoint)
        self._add_cdn_endpoint(bucket_name, cdn_endpoint)

    def object_exists(self, key):
        """
        如果文件存在就返回True，否则返回False。如果Bucket不存在，或是发生其他错误，则抛出异常。
        :param key:
        :return:
        """
        return self._do_object_exists(key)

    def put_object(self, data,
                   key='',
                   headers=None,
                   progress_callback=None):
        """
        上传一个普通文件。
        :param key:
        :param data:
        :param headers:
        :param progress_callback:
        :return:
        """
        # 如果未指定key, 需要根据md5设置key值
        storage_path = key if key else self._get_storage_path(data)

        # 当key值是根据md5计算时,先判断是否已存在. 如是则无需重复上传.
        if storage_path != key and self.object_exists(storage_path):
            return storage_path

        if isinstance(data, str) and os.path.exists(data):
            data = open(data, 'rb')
        else:
            data.seek(0)

        return self._do_put_object(storage_path, data, headers, progress_callback)

    def delete_object(self, key):
        """
        删除一个文件
        :param key:
        :return:
        """
        return self._do_delete_object(key)

    def list_objects(self, prefix='', delimiter='', marker='', max_keys=100):
        """根据前缀罗列Bucket里的文件。

        :param str prefix: 只罗列文件名为该前缀的文件
        :param str delimiter: 分隔符。可以用来模拟目录
        :param str marker: 分页标志。首次调用传空串，后续使用返回值的next_marker
        :param int max_keys: 最多返回文件的个数，文件和目录的和不能超过该值
        """
        return self._list_objects(prefix=prefix, delimiter=delimiter, marker=marker, max_keys=max_keys)

    def get_object_meta(self, key):
        """
        获取文件基本元信息
        :param key:
        :return:
        """
        return self._do_get_object_meta(key)

    @classmethod
    def get_image_url(cls, src, bucket_name, endpoint='', cdn_endpoint=''):
        if not endpoint:
            endpoints = cls._endpoints.get(cls.__name__)


    def _add_endpoint(self, bucket_name, endpoint):
        if not bucket_name or not endpoint:
            return

        class_name = self.__class__.__name__
        if class_name not in self._endpoints:
            class_endpoints = {}
            self._endpoints[class_name] = class_endpoints

        class_endpoints = self._endpoints[class_name]
        class_endpoints['bucket_name'] = endpoint

    def _add_cdn_endpoint(self, bucket_name, cdn_endpoint):
        if not bucket_name or not cdn_endpoint:
            return

        class_name = self.__class__.__name__
        if class_name not in self._cdn_endpoints:
            class_cdn_endpoints = {}
            self._cdn_endpoints[class_name] = class_cdn_endpoints

            class_cdn_endpoints = self._cdn_endpoints[class_name]
        class_cdn_endpoints['bucket_name'] = cdn_endpoint

    def _get_file_md5(self, input_file):
        input_file.seek(0)
        md5_string = hashlib.md5(input_file.read()).hexdigest()
        return md5_string

    def _get_image_storage_path(self, data, md5_string):
        if isinstance(file, Image.Image):
            image = file
        else:
            image = Image.open(data)

        format = image.format.lower()
        storage_path = "{0}/{1}/{2}.{3}".format(md5_string[:2], md5_string[2:4], md5_string, format)
        return storage_path

    def _get_file_storage_path(self, filename, extension, md5_string):
        if extension:
            storage_path = "{0}/{1}/{2}{3}".format(md5_string[:2], md5_string[2:4], md5_string, extension)
        else:
            storage_path = "{0}/{1}/{2}".format(md5_string[:2], md5_string[2:4], md5_string)
        return storage_path

    def _get_storage_path(self, data):
        filename = ''
        extension = ''
        if hasattr(data, 'filename'):
            filename = getattr(data, 'filename', None)
            _, extension = os.path.splitext(filename)

        md5_string = self._get_file_md5(data)

        # #图片
        # if extension and extension.lower() in self._IMAGES_ALLOWED:
        #     return self._get_image_storage_path(data, md5_string)
        return self._get_file_storage_path(filename, extension, md5_string)


class AliyunBucket(_BucketBase):

    def __init__(self, access_key_id, access_key_secret, bucket_name, endpoint='', cdn_endpoint=''):
        super(AliyunBucket, self).__init__(access_key_id, access_key_secret, bucket_name, endpoint, cdn_endpoint)

        self.auth = oss2.Auth(access_key_id, access_key_secret)
        self.bucket = oss2.Bucket(self.auth, endpoint, bucket_name)

    @aliyun_list_result_handler
    def _list_objects(self, prefix, delimiter, marker, max_keys):
        return self.bucket.list_objects(prefix=prefix, delimiter=delimiter, marker=marker, max_keys=max_keys)

    def _do_object_exists(self, key):
        """

        :param key:
        :return:
        """
        return self.bucket.object_exists(key)

    def _do_put_object(self, key, data,
                   headers=None,
                   progress_callback=None):
        """

        :param data:
        :param headers:
        :param progress_callback:
        :return:
        """
        result = self.bucket.put_object(key, data, headers=headers, progress_callback=progress_callback)
        return key if result.etag != '' else None

    def _do_delete_object(self, key):
        return self.bucket.delete_object(key)


class QiniuBucket(_BucketBase):
    def __init__(self, access_key_id, access_key_secret, bucket_name, endpoint='', cdn_endpoint=''):
        super(QiniuBucket, self).__init__(access_key_id, access_key_secret, bucket_name, endpoint, cdn_endpoint)

        self.bucket_name = bucket_name
        self.auth = qiniu.Auth(access_key_id, access_key_secret)
        self.bucket = qiniu.BucketManager(self.auth)

    @qiniu_list_result_handler
    def _list_objects(self, prefix, delimiter, marker, max_keys):
        return self.bucket.list(self.bucket_name, prefix=prefix, delimiter=delimiter, marker=marker, limit=max_keys)

    @qiniu_bool_result_handler
    def _do_object_exists(self, key):
        """

        :param key:
        :return:
        """
        return self.bucket.stat(self.bucket_name, key)

    @qiniu_bool_result_handler
    @qiniu_error_handler
    def __do_put_object(self, key, data,
                   headers=None,
                   progress_callback=None):
        """
        """
        token = self.auth.upload_token(self.bucket_name, key, 3600)
        return qiniu.put_data(token, key, data, progress_handler=progress_callback)

    def _do_put_object(self, key, data,
                   headers=None,
                   progress_callback=None):
        ret = self.__do_put_object(key, data, headers, progress_callback)
        return key if ret else None

    @qiniu_result_handler
    @qiniu_error_handler
    def _do_get_object_meta(self, key):
        return self.bucket.stat(self.bucket_name, key)

    @qiniu_bool_result_handler
    @qiniu_error_handler
    def _do_delete_object(self, key):
        return self.bucket.delete(self.bucket_name, key)


class QcloudBucket(_BucketBase):
    def __init__(self, access_key_id, access_key_secret, region, bucket_name, token='', endpoint='', cdn_endpoint=''):
        super(QcloudBucket, self).__init__(access_key_id, access_key_secret, bucket_name, endpoint, cdn_endpoint)

        self.config = qcloud_cos.CosConfig(Secret_id=access_key_id, Secret_key=access_key_secret, Region=region, Token=token)
        self.client = qcloud_cos.CosS3Client(self.config)
        self.bucket_name = bucket_name

    def _list_objects(self, prefix, delimiter, marker, max_keys):
        return self.client.list_objects(Bucket=self.bucket_name, MaxKeys=max_keys, Prefix=prefix, Delimiter=delimiter)

    def _do_object_exists(self, key):
        """

        :param key:
        :return:
        """
        try:
            response = self.client.head_object(
                Bucket=self.bucket_name,
                Key=key,
                IfModifiedSince='string'
            )
        except qcloud_cos.CosServiceError as e:
            return False

        if response:
            return 'ETag' in response
        return False

    def _do_put_object(self, key, data,
                   headers=None,
                   progress_callback=None):
        """

        :param data:
        :param headers:
        :param progress_callback:
        :return:
        """
        response = self.client.put_object(
            Bucket=self.bucket_name,  # Bucket由bucketname-appid组成
            Body=data,
            Key=key,
            StorageClass='STANDARD',
            CacheControl='no-cache'
        )
        if response:
            # return 'ETag' in response
            return key
        return None

    def _do_delete_object(self, key):
        response = self.client.delete_object(
            Bucket=self.bucket_name,
            Key=key
        )
        return True