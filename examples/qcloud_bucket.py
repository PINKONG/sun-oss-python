# -*- coding: utf-8 -*-

import os
import sys

sys.path.append('..')
from sun_oss import *

access_key_id = os.getenv('TENTCENT_OSS_ACCESS_KEY_ID', '<你的AccessKeyId>')
access_key_secret = os.getenv('TENTCENT_OSS_ACCESS_KEY_SECRET', '<你的AccessKeySecret>')
region = os.getenv('TENTCENT_REGION', '<你的Region>')

bucket_name = 'tx-image-1256055725'

# 确认上面的参数都填写正确了
for param in (access_key_id, access_key_secret, bucket_name, region):
    assert '<' not in param, '请设置参数：' + param

bucket = get_qcloud_bucket(access_key_id, access_key_secret, region, bucket_name)


def upload():
    with open("gogopher.jpg", 'rb') as f:
        ret = bucket.put_object(f)
        print ret


if __name__ == '__main__':
    upload()
