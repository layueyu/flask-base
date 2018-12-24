"""
蓝图定义
"""

from flask import Blueprint

api = Blueprint('api_1_0', __name__)

# 加载视图
from .sys.views import verify_code, sys_login, sys_user


# 加载模型
from .sys import models
