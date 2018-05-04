# -*- coding: utf-8 -*-

__author__ = 'pinkong'


from .bucket import AliyunBucket, QiniuBucket, QcloudBucket


def get_qiniu_server(bucket_name):
    pass


def get_qiniu_bucket(access_key_id, access_key_secret, bucket_name, endpoint='', cdn_endpoint=''):
    bucket = QiniuBucket(access_key_id=access_key_id, access_key_secret=access_key_secret, bucket_name=bucket_name, endpoint=endpoint, cdn_endpoint=cdn_endpoint)
    return bucket


def get_aliyun_server():
    pass


def get_aliyun_bucket(access_key_id, access_key_secret, bucket_name, endpoint='', cdn_endpoint=''):
    bucket = AliyunBucket(access_key_id=access_key_id, access_key_secret=access_key_secret, bucket_name=bucket_name, endpoint=endpoint, cdn_endpoint=cdn_endpoint)
    return bucket


def get_qcloud_server():
    pass


def get_qcloud_bucket(access_key_id, access_key_secret, region, bucket_name, endpoint='', cdn_endpoint=''):
    bucket = QcloudBucket(access_key_id=access_key_id, access_key_secret=access_key_secret, region=region, bucket_name=bucket_name, endpoint=endpoint, cdn_endpoint=cdn_endpoint)
    return bucket
