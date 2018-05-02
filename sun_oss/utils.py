# -*- coding: utf-8 -*-


import os
import oss2
from .api import AliyunBucket, QiniuBucket, QcloudBucket


def get_qiniu_server(bucket_name):
    pass


def get_qiniu_bucket(access_key_id, access_key_secret, bucket_name):
    bucket = QiniuBucket(access_key_id, access_key_secret, bucket_name)
    return bucket


def get_aliyun_server():
    pass


def get_aliyun_bucket(access_key_id, access_key_secret, endpoint, bucket_name):
    bucket = AliyunBucket(access_key_id, access_key_secret, endpoint, bucket_name)
    return bucket


def get_qcloud_server():
    pass


def get_qcloud_bucket(access_key_id, access_key_secret, region, bucket_name):
    bucket = QcloudBucket(access_key_id, access_key_secret, region, bucket_name)
    return bucket

