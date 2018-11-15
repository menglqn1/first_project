from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf import CSRFProtect

app = Flask(__name__)


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


app.config.from_object(Config)
db = SQLAlchemy(app)
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_POST)
CSRFProtect(app)
Session(app)
manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)


@app.route('/')
def index():
    return 'Hello World'


if __name__ == '__main__':
    app.run()
