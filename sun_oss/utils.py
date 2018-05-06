# -*- coding: utf-8 -*-


import os
import oss2
import re
from functools import wraps
from oss2.models import ListObjectsResult


def normalize_endpoint(endpoint):
    if endpoint and not endpoint.startswith('http://') and not endpoint.startswith('https://'):
        return 'http://' + endpoint
    else:
        return endpoint


def qiniu_result_handler(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        ret, info = func(*args, **kwargs)
        return ret

    return decorator


__QINIU_NULL_SUCCESS_FUC = {'_do_delete_object', '_do_rename_object', '_do_rename_object', '_do_move_object',
                             '_do_copy_object', '_do_fetch_object', '_do_prefetch_object'}


def qiniu_bool_result_handler(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        ret, info = func(*args, **kwargs)

        if ret:
            return 'hash' in ret

        # 成功返回NULL
        if func.__name__ in __QINIU_NULL_SUCCESS_FUC:
            return True

        return False

    return decorator


def qiniu_list_result_handler(func):
    """
    将ListObjectsResult转为字典
    :param func:
    :return:
    """
    @wraps(func)
    def decorator(*args, **kwargs):
        ret, eof, info = func(*args, **kwargs)

        response = {}
        response['IsTruncated'] = False if ret and not ret.get('marker') else True
        response['NextMarker'] = '' if not ret.get('marker') else ret.get('marker')

        object_list = []
        for object_info in ret['items']:
            info = {}
            info['Key'] = object_info.get('key')
            info['LastModified'] = object_info.get('putTime')
            info['ETag'] = object_info.get('hash')
            info['Size'] = object_info.get('fsize')
            info['StorageClass'] = object_info.get('type')
            object_list.append(info)
            response['Contents'] = object_list

        return response

    return decorator


def aliyun_list_result_handler(func):
    """
    将ListObjectsResult转为字典
    :param func:
    :return:
    """
    @wraps(func)
    def decorator(*args, **kwargs):
        result = func(*args, **kwargs)

        if isinstance(result, ListObjectsResult):
            ret = {}
            ret['IsTruncated'] = result.is_truncated
            ret['NextMarker'] = result.next_marker

            object_list = []
            for object_info in result.object_list:
                info = {}
                info['Key'] = object_info.key
                info['LastModified'] = object_info.last_modified
                info['ETag'] = object_info.etag
                info['Size'] = object_info.size
                info['StorageClass'] = object_info.storage_class
                object_list.append(info)
            ret['Contents'] = object_list

            return ret

        return None

    return decorator


thumbnail_regex = re.compile(r'thumbnail/(w)/(\d{2,4})\b')


def get_image_thumbnail_processing(processing):
    """
    返回缩略图宽度
    :param processing:
    :return:
    """
    if processing:
        ret = thumbnail_regex.search(processing)
        if ret:
            return ret.group(2)
    return None


def get_image_corp_processing(processing):
    return None


def get_image_rotate_processing(processing):
    return None


def get_image_blur_processing(processing):
    return None

