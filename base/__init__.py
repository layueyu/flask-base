"""
项目初始化
"""
from flask import Flask
from flask_script import Manager
from flask_session import Session
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from logging.handlers import RotatingFileHandler
import redis
import logging
import pymysql

from setting import setting_map


# 全局属性 #

# 数据库对象
db_ = None

# redis 连接对象
redis_ = None


def __create_app(setting_class):
    """
    创建 flask 实例
    :return:
    """
    _app = Flask(__name__)

    # 根据配置模式名字获取配置参数类
    _app.config.from_object(setting_class)

    # 补充csrf防护
    CSRFProtect(_app)

    return _app


def __init_db(app):
    """
    初始化 数据库
    :return:
    """
    pymysql.install_as_MySQLdb()

    return SQLAlchemy(app)


def __init_redis(setting_class):
    """
    初始化 redis
    :return:
    """
    return redis.StrictRedis(
        host=setting_class.REDIS_HOST,
        port=setting_class.REDIS_PORT,
        db=setting_class.REDIS_DB
    )


def __init_session(app):
    """
    初始化 session
    :return:
    """
    Session(app=app)


def __init_manager(app, db):
    """
    初始化 manager
    :return:
    """
    _manager = Manager(app)

    # 配置数据库命令
    Migrate(app, db)
    _manager.add_command('db', MigrateCommand)

    return _manager


def __reg_blueprint(app):
    """
    注册 蓝图
    :return:
    """
    # API 蓝图
    from base import api_1_0
    app.register_blueprint(api_1_0.api, url_prefix='/api/v1.0')


def __init_logging(setting_class):
    """
    日志初始化 记录到文集
    :return:
    """

    # 设置日志记录等级
    logging.basicConfig(level=setting_class.LOGGING_LEVEL)

    # 创建日志记录器，指明日志保存路径、每个日志最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler(
        filename=setting_class.LOGGING_FILE,
        maxBytes=setting_class.LOGGING_MAX_BYTES,
        backupCount=setting_class.LOGGING_COUNT
    )

    # 创建日志记录的格式
    formatter = logging.Formatter(setting_class.LOGGING_FORMAT)

    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)

    # 为全局的日志工具对象添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


def __init_converter(app):
    """
    配置 自定以转换器
    :return:
    """
    from base.commons.converter import ReConverter, MobileConverter
    app.url_map.converters['re'] = ReConverter
    app.url_map.converters['mobile'] = MobileConverter


def init(env_name='dev'):
    """初始化配置"""
    _setting_class = setting_map.get(env_name)

    # 创建实例
    _app = __create_app(setting_class=_setting_class)

    # 创建数据库
    _db = __init_db(app=_app)
    global db_
    db_ = _db

    # 初始化redis连接
    _redis = __init_redis(setting_class=_setting_class)
    global redis_
    redis_ = _redis

    # 初始化配置-初始化session
    __init_session(app=_app)

    # 初始化配置-初始化manager
    _manager = __init_manager(app=_app, db=_db)

    # 初始化配置-初始化日志
    __init_logging(setting_class=_setting_class)

    # 添加自定以转换器
    __init_converter(app=_app)

    # 初始化配置-注册蓝图
    __reg_blueprint(app=_app)

    return _app, _manager
