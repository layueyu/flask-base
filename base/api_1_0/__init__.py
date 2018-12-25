"""
蓝图定义
"""

from datetime import datetime
from flask import Blueprint, request, current_app, g
from base.commons.response import R, RET
from .filter import OauthFilter
api = Blueprint('api_1_0', __name__, url_prefix='/api/v1.0')


# 加载视图
from .sys.views import verify_code, sys_login, sys_user

# 加载模型
from .sys import models as sys_models
from .demo import models as demo_models


# 定义钩子函数
@api.before_request
def check_token():

    oauth_str = OauthFilter.check_url_oauth(request.path)

    if oauth_str != 'anon':
        token = request.headers.get('token')
        if token is None:
            token = request.args.get('token')
        try:
            user_token = sys_models.UserToken.query.filter_by(token=token).first()
        except Exception as e:
            current_app.logger.error(e)
            return R.err(RET.TOKENINVALID, 'token 失效')
        else:
            if user_token is None:
                return R.err(RET.TOKENINVALID, 'token 失效')

            if datetime.now() >= user_token.expire_time:
                return R.err(RET.TOKENINVALID, 'token 失效')
            # 传递参数
            g.user_id = user_token.user.id
