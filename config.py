import redis


class Config:
    """工程配置信息"""
    SECRET_KEY = 'EjpNVSNQTyGi1VvWECj9TvC/+kq3oujee2kTfQUs8yCM6xX9Yjq52v54g+HVoknA'
    DEBUG = True

    # 数据库配置信息
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@172.0.0.1:3306/'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # redis配置
    REDIS_HOST = '127.0.0.1'
    REDIS_POST = '6379'

    # flask-session的配置信息
    SESSION_TYPE = 'redis'  # 指定 session 保存到 redis 中
    SESSION_USE_SIGNER = True  # 让 cookie 中的 session_id 被加密签名处理
    # 创建redis实例
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_POST)
    PERMANENT_SESSION_LIFETIME = 86400  # session有效期
