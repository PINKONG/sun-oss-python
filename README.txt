A Simple OSS SDK Integration. Include Aliyun, Qiniu, Qcloud, Maybe more

Very Easy for use!

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

    #upload
    ret = ali_bucket.put_object(upload_file)

github: https://github.com/PINKONG/sun-oss-python