"""
用户信息 视图函数
"""

import re
from flask import request, current_app
from sqlalchemy.exc import IntegrityError

from base import redis_, db_

from base.commons.response import R, RET
from base.commons import regex
from base.commons.keys import RedisKeys

from base.api_1_0 import api
from base.api_1_0.sys.models import User


@api.route('/user/add', methods=['POST'])
def add():
    """
    添加用户
    参数格式： JSON
    :return:
    """

    # 获取前端JSON数据，返回字典
    req_dict = request.get_json()

    user_name = req_dict.get('user_name')
    image_code = req_dict.get('image_code')
    image_code_id = req_dict.get('image_code_id')
    password = req_dict.get('password')
    password2 = req_dict.get('password2')

    name = req_dict.get('name')
    mobile = req_dict.get('mobile')
    avatar_url = req_dict.get('avatar_url')

    # 校验参数
    if not all([user_name, image_code, password]):
        return R.err(RET.PARAMERR, '参数不完整')

    # 密码校验
    if password != password2:
        return R.err(RET.PARAMERR, '两次输入密码不一致')

    # 判断手机号格式
    if mobile is not None:
        if not re.match(regex.MOBILE_RE, mobile):
            return R.err(RET.PARAMERR, '手机号格式错误')

    # 取出图片验证码
    try:
        real_image_code = redis_.get(RedisKeys.image_code_key(image_code_id))
    except Exception as e:
        current_app.logger.error(e)
        return R.err(RET.DBERR, '读取真实图片验证码异常')

    # 判断图片验证码
    if real_image_code is None:
        return R.err(RET.NODATA, '图片验证码失效')

    # 判断用户填写的图片验证码
    if real_image_code.upper().decode('ascii') != image_code.upper():
        return R.err(RET.DATAERR, "图片验证码错误")

    # 删除redis中的短信验证码，防止重复使用
    try:
        redis_.delete(RedisKeys.image_code_key(image_code_id))
    except Exception as e:
        current_app.logger.error(e)

    # 保存用户数据
    user = User()

    user.user_name = user_name
    user.mobile = mobile
    user.name = name
    user.avatar_url = avatar_url

    user.password = password
    try:
        db_.session.add(user)
        db_.session.commit()
    except IntegrityError as e:
        # 数据库操作失败后回滚
        db_.session.rollback()
        # 表示出现重复值
        current_app.logger.error(e)
        return R.err(RET.DATAEXIST, '用户名以存在')
    except Exception as e:
        # 数据库操作失败后回滚
        db_.session.rollback()
        current_app.logger.error(e)
        return R.err(RET.DBERR, '数据库异常')

    return R.ok('注册成功')
