"""
静态文件-路径
"""
from flask import Blueprint, current_app, make_response

static_api = Blueprint('web_static', __name__)


@static_api.route("/<file_name>")
def get_html(file_name):
    """
    提供html文件
    """
    file_name = 'static/' + file_name

    # flask 提供返回静态文集的方法
    resp = make_response(current_app.send_static_file(file_name))

    return resp
