# -*- coding: utf-8 -*-

import os
import sys

sys.path.append('..')
from sun_oss import *

access_key_id = os.getenv('QINIU_OSS_ACCESS_KEY_ID', 'Y7DfWVC6orXL2SuM8NT96Po_NNEMzaYX_ZNw2C1I')
access_key_secret = os.getenv('QINIU_OSS_ACCESS_KEY_SECRET', 'CEmMvh_NRjohQ78LQF82oqEYC3HsEOcpl5T7nZef')

bucket_name = 'pk-image'

# 确认上面的参数都填写正确了
for param in (access_key_id, access_key_secret, bucket_name):
    assert '<' not in param, '请设置参数：' + param

bucket = get_qiniu_bucket(access_key_id, access_key_secret, bucket_name)


def upload():
    with open("gogopher.jpg", 'rb') as f:
        ret = bucket.put_object(f)
        print ret


if __name__ == '__main__':
    upload()
