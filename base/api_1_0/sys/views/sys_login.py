"""
登录模块
"""

from flask import request, current_app
from base.commons.response import R, RET
from base.commons.keys import RedisKeys
from base.commons import constants
from base.commons.utils.oauth_utils import TokenUtil
from base import redis_, db_
from base.api_1_0 import api
from base.api_1_0.sys.models import User, UserToken


@api.route('/login', methods=['POST'])
def login():
    """
    用户登陆
    参数： 用户名，密码，验证码
    """
    req_dict = request.get_json()

    user_name = req_dict.get('user_name')
    password = req_dict.get('password')
    image_code = req_dict.get('image_code')
    image_code_id = req_dict.get('image_code_id')

    # 校验参数
    if not all([user_name, password, image_code, image_code_id]):
        return R.err(RET.PARAMERR, '参数不完整')

    # 判断验证码
    try:
        real_image_code = redis_.get(RedisKeys.image_code_key(image_code_id))
    except Exception as e:
        current_app.logger.error(e)
        return R.err(RET.DBERR, 'redis数据库异常')

    # 判断图片验证码是否过期
    if real_image_code is None:
        return R.err(RET.DBERR, '图片验证码失效')

    # 删除 图片验证码
    try:
        redis_.delete(RedisKeys.image_code_key(image_code_id))
    except Exception as e:
        current_app.logger.error(e)

    # 对比用户输入
    if real_image_code.upper().decode('ascii') != image_code.upper():
        return R.err(RET.DATAERR, '验证码错误')

    # 判断错误次属是否超过限制，如果超过限制则返回
    user_ip = request.remote_addr  # 用户的IP地址

    try:
        access_nums = redis_.get(RedisKeys.access_err_num_key(user_ip))
    except Exception as e:
        current_app.logger.error(e)
    else:
        if access_nums is not None and int(access_nums) >= constants.LOGIN_ERROR_MAX_TIMES:
            return R.err(RET.REQERR, '错误次数过多，请稍后重试')

    try:
        user = User.query.filter_by(user_name=user_name).first()
    except Exception as e:
        current_app.logger.error(e)
        return R.err(RET.DBERR, '获取用户信息失败')

    if user is None or not user.check_password(password):
        try:
            redis_.incr(RedisKeys.access_err_num_key(user_ip))
            redis_.expire(RedisKeys.access_err_num_key(user_ip), constants.LOGIN_ERROR_FORBID_TIME)
        except Exception as e:
            current_app.logger.error(e)
        return R.err(RET.DATAERR, '用户名或密码错误')

    # 校验用户是否生成token
    user_token = None
    try:
        user_token = UserToken.query.filter(user_id=user.id).first()
    except Exception as e:
        current_app.logger.error(e)

    # 生成 token
    token_data, expire_time = TokenUtil.create_token(user_name=user.user_name, user_id=user.id)

    # 判断 是否生成token
    if user_token is None:
        try:
            user_token = UserToken()
            user_token.user_id = user.id
            user_token.token = token_data
            user_token.expire_time = expire_time

            db_.session.add(user_token)
            db_.session.commit()
        except Exception as e:
            db_.session.rollback()
            current_app.logger.error(e)
            return R.err(RET.DBERR, '数据库异常')
    else:
        user_token.token = token_data
        user_token.expire_time = expire_time

        try:
            db_.session.commit
        except Exception as e:
            db_.session.rollback()
            current_app.logger.error(e)
            return R.err(RET.DBERR, '数据库异常')

    # 生成result
    result_data = {
        'token': token_data,
        'expire_time': expire_time
    }
    return R.ok('登录成功', result_data)
