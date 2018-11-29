# appid 已在配置中移除,请在参数 Bucket 中带上 appid。Bucket 由 bucketname-appid 组成
# 1. 设置用户配置, 包括 secretId，secretKey 以及 Region
# -*- coding=utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

secret_id = 'AKID9IHAtcVsPLakpttvhlHhyBF9weBPZeij'      # 替换为用户的 secretId
secret_key = '6HOjwDh7NJNTUVXewFWr55DQXWVTffcQ'      # 替换为用户的 secretKey
region = 'ap-chengdu'     # 替换为用户的 Region
token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
# 2. 获取客户端对象
client = CosS3Client(config)
# 参照下文的描述。或者参照 Demo 程序，详见 https://github.com/tencentyun/cos-python-sdk-v5/blob/master/qcloud_cos/demo.py


def storage(data, file_name):
    try:
        response = client.put_object(
            Bucket='menglq-1256694994',
            Body=data,
            Key='news/' + file_name,
        )
        print(response['ETag'])
    except Exception as e:
        raise e
    if not response['ETag']:
        raise Exception('上传文件失败')


if __name__ == '__main__':
    file = input('输入文件路径：')
    file_name = '111avt'
    with open(file, 'rb') as f:
        storage(f.read(),file_name)