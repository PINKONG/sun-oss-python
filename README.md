# SUN OS

封装了aliyun、七牛、腾讯云等对象存储sdk，提供一致性的操作界面。

## Install

```bash
pip install sun_oss
```


## Usage

#### 初始化
在你需要的地方

```python
    from sun_oss import get_aliyun_bucket, get_qiniu_bucket, get_qcloud_bucket

    # aliyun
    access_key_id = os.getenv('ALI_OSS_ACCESS_KEY_ID', '<your ALI_OSS_ACCESS_KEY_ID>')
    access_key_secret = os.getenv('ALI_OSS_ACCESS_KEY_SECRET', '<your ALI_OSS_ACCESS_KEY_SECRET>')
    endpoint = os.getenv('ALI_OSS_ENDPOINT', '<your ALI_OSS_ENDPOINT>')
    bucket_name = os.getenv('BUCKET_NAME', '<your BUCKET-NAME>')
    ali_bucket = get_aliyun_bucket(access_key_id, access_key_secret, bucket_name, endpoint)

    #qiniu
    access_key_id = os.getenv('QINIU_OSS_ACCESS_KEY_ID', '<your QINIU_OSS_ACCESS_KEY_ID>')
    access_key_secret = os.getenv('QINIU_OSS_ACCESS_KEY_SECRET', '<your QINIU_OSS_ACCESS_KEY_SECRET>')
    bucket_name = os.getenv('BUCKET_NAME', '<your BUCKET-NAME>')
    qiniu_bucket = get_qiniu_bucket(access_key_id, access_key_secret, bucket_name)


    access_key_id = os.getenv('TENTCENT_OSS_ACCESS_KEY_ID', '<your TENTCENT_OSS_ACCESS_KEY_ID>')
    access_key_secret = os.getenv('TENTCENT_OSS_ACCESS_KEY_SECRET', '<your TENTCENT_OSS_ACCESS_KEY_SECRET>')
    region = os.getenv('TENTCENT_REGION', '<your BUCKET-NAME>')
    qcloud_bucket = get_qcloud_bucket(access_key_id, access_key_secret, region, bucket_name)

```


之后就可以通过bucket对象来进行操作.


#### 列出一个bucket中的所有文件
```python
bucket.list_objects()
```
这个方法还有 marker, limit, prefix这三个可选参数，详情参考官方文档


#### 上传

```python
ret = bucket.put_object(upload_file)
```


#### 删除，查看文件信息
```python
bucket.get_object_meta('a')              # 查看单个文件信息
bucket.delete_object('a')               # 删除单个文件
```


## TODO:

