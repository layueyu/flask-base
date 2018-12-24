"""
配置文件
"""
import redis
import logging


class Config(object):
    """BASE 配置信息"""

    SECRET_KEY = '5c79a5a204d6800778fc71527a379ed227fefeb4c598a7d35abaf114cbe75784-zero.org'

    # 数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # session
    SESSION_TYPE = 'redis'
    SESSION_USE_SIGNER = True  # 对cookie中的session id 进行隐藏
    PERMANENT_SESSION_LIFETIME = 86400  # session 有效期，单位秒

    # logging
    LOGGING_FILE = 'logs/logs'
    LOGGING_MAX_BYTES = 1024*1024*1024
    LOGGING_COUNT = 10
    LOGGING_FORMAT = '%(asctime)s === %(levelname)s === %(filename)s:%(lineno)d ===::: %(message)s'


class DevConfig(Config):
    """开发环境配置"""
    DEBUG = True

    # 数据库
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:zero28!@127.0.0.1:3306/base'
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/base'

    # Redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_DB = 14

    # Session
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

    # logging
    LOGGING_LEVEL = logging.DEBUG


class ProConfig(Config):
    """运行环境配置"""
    # 数据库
    SQLALCHEMY_DATABASE_URI = 'mysql://root:zero28!@127.0.0.1:3306/base'
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/base'

    # Redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_DB = 14

    # Session
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

    # logging
    LOGGING_LEVEL = logging.INFO


setting_map = {
    'dev': DevConfig,
    'pro': ProConfig
}
