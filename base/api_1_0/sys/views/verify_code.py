"""
验证码-视图模块
"""

from flask import current_app, make_response
from flask_wtf import csrf

from base import redis_
from base.api_1_0 import api
from base.commons import constants
from base.commons.keys import RedisKeys
from base.commons.response import RET, R
from base.commons.utils.captcha.captcha import Captcha


@api.route('/image_codes/<uuid>', methods=['GET'])
def get_image_code(uuid):
    """
    图片验证码
    :param uuid: 验证码编号， UUID
    :return:
    """
    # 生成验证码图片
    captcha = Captcha()

    # 名字， 真实文本， 图片数据
    name, text, image_data = captcha.generate_captcha()

    # 将验证码保存到redis中
    try:
        redis_.setex(RedisKeys.image_code_key(uuid), constants.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        current_app.logger.error(e)
        return R.err(RET.DBERR, '保存图片验证码失败')

    # 创建返回对象
    resp_ = make_response(image_data)
    resp_.headers['Content-Type'] = 'image/jpg'

    # 设置cookie值， csrf防护
    resp_.set_cookie('csrf_token', csrf.generate_csrf())

    return resp_
