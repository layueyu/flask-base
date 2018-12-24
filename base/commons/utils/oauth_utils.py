"""
自定义令牌
"""
import uuid
import time
from datetime import datetime

from flask import current_app
from base.commons.utils.code_utils import hl_sha256
from base.commons import constants


class TokenUtil:
    """
    token 生成工具
    """

    @classmethod
    def create_token(cls, user_name='0', user_id=0):
        """
        生成 token
        :param user_name: 用户名
        :param user_id: 用户id
        :return: token
        """

        # 生成 token
        data = '{}-{}-{}'.format(uuid.uuid1(), user_name, user_id)
        token_data = hl_sha256(current_app.config.get('SECRET_KEY'), data)

        # 过期时间
        expire_time = datetime.fromtimestamp(time.time() + constants.TOKEN_TIME_EXPIRES)

        return token_data, expire_time

