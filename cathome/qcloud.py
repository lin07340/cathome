# -*-coding: UTF-8 -*-

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging
from cathome import app

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

secret_id = 'AKIDtZz92gVB3ez4tTvxqVw86pJZaMtBO2cw'  # 替换为用户的 secretId
secret_key = 'DBtMZWEVWHm35sRlqfFZdRzHZcOuA9sK'  # 替换为用户的 secretKey
region = 'ap-guangzhou'  # 替换为用户的 Region
token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
# 2. 获取客户端对象
client = CosS3Client(config)


def save_to_cloud(file, file_name):
    response = client.put_object(
        Bucket='cathome-1257654472',
        Body=file.stream,
        Key=file_name,
    )
    print(response['ETag'])
    return app.config['DOMAIN'] + file_name
