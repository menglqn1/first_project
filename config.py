import logging

import redis


class Config:
    """工程配置信息"""
    SECRET_KEY = 'EjpNVSNQTyGi1VvWECj9TvC/+kq3oujee2kTfQUs8yCM6xX9Yjq52v54g+HVoknA'

    # 数据库配置信息
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/information'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # redis配置
    REDIS_HOST = '127.0.0.1'
    REDIS_POST = '6379'

    # flask-session的配置信息
    SESSION_TYPE = 'redis'  # 指定 session 保存到 redis 中
    SESSION_USE_SIGNER = True  # 让 cookie 中的 session_id 被加密签名处理
    # 创建redis实例
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_POST)
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = 86400  # session有效期

    LOG_LEVEL = logging.DEBUG


class DevelopmentConfig(Config):
    """开发模式下配置"""
    DEBUG = True


class ProductionConfig(Config):
    """生产模式配置"""
    DEBUG = False
    LOG_LEVEL = logging.ERROR


class TestingConfig(Config):
    """单元测试环境下的配置"""
    DEBUG = True
    TESTING = True


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}
