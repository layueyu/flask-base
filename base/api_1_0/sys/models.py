"""
模型
"""

from werkzeug.security import generate_password_hash, check_password_hash

from base import db_
from base.api_1_0.base.base import BaseModel


class User(BaseModel, db_.Model):
    """用户信息"""

    __tablename__ = "sys_user"

    id = db_.Column(db_.Integer, primary_key=True)  # 用户编号
    user_name = db_.Column(db_.String(32), unique=True, nullable=False)  # 登录名
    password_hash = db_.Column(db_.String(256), nullable=False)  # 加密的密码
    name = db_.Column(db_.String(32))  # 用户姓名
    mobile = db_.Column(db_.String(11))  # 手机号
    avatar_url = db_.Column(db_.String(256))  # 用户头像路径

    token = db_.relationship("UserToken", backref="user")  # 用户token

    #  @property  将方法变为属性
    @property
    def password(self):
        """
        读取 user.password
        """
        raise AttributeError("这个属性只能设置，不能读取")

    # 对应设置属性操作
    @password.setter
    def password(self, value):
        """
        设置 user.password = xxx
        :param value: 密码值
        :return:
        """
        # 对密码进行加密
        self.password_hash = generate_password_hash(value)

    def check_password(self, value):
        """
        检验密码的正确性
        :param value: 用户登录时填写的原始密码
        :return:
        """
        return check_password_hash(self.password_hash, value)

    def to_dict(self):
        """转换 字典"""
        return {
            'id': self.id,
            'user_name': self.user_name,
            'name': self.name,
            'mobile': self.mobile,
            'avatar_url': self.avatar_url
        }


class UserToken(BaseModel, db_.Model):
    """
    用户 TOKEN 关联关系
    """
    __tablename__ = "sys_user_token"

    user_id = db_.Column(db_.Integer, db_.ForeignKey('sys_user.id'), primary_key=True)  # 用户编号
    token = db_.Column(db_.String(300), nullable=False)  # token 值
    expire_time = db_.Column(db_.DateTime, nullable=False)  # 过期时间
