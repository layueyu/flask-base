"""
用户信息 视图函数
"""

import re
from flask import request, current_app, g
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

from base import redis_, db_

from base.commons.response import R, RET
from base.commons import regex
from base.commons.keys import RedisKeys
from base.commons.page import Page
from base.api_1_0 import api
from base.api_1_0.sys.models import User


@api.route('/user/page_list')
def page_list():
    """
    分页查询
    :return:
    """

    page = Page()

    page.page = request.args.get('page')
    page.limit = request.args.get('limit')
    user_name = request.args.get('user_name')

    # 过滤条件的参数容器
    filter_params = []

    # 用户名
    if user_name:
        filter_params.append(User.user_name.ilike('%{}%'.format(user_name)))

    # 排序条件
    house_query = User.query.filter(*filter_params).order_by(User.create_time.desc())

    # 处理分页
    try:
        page_obj = house_query.paginate(page=page.page, per_page=page.limit, error_out=False)
    except Exception as e:
        current_app.logger.error(e)
        return R.err(RET.DBERR, '数据库异常')

    # 获取页面数据
    user_li = page_obj.items
    users = [user.to_dict() for user in user_li]
    page.list = users

    # 总页数
    page.total_page = page_obj.pages

    # 总条数
    page.total_count = page_obj.total

    return R.ok('OK', page.to_dict())


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


@api.route('/user/update', methods=['POST'])
def update():
    """
    修改用户
    参数格式： JSON
    :return:
    """

    # 获取前端JSON数据，返回字典
    req_dict = request.get_json()

    name = req_dict.get('name')
    mobile = req_dict.get('mobile')
    avatar_url = req_dict.get('avatar_url')

    # 判断手机号格式
    if mobile is not None:
        if not re.match(regex.MOBILE_RE, mobile):
            return R.err(RET.PARAMERR, '手机号格式错误')

    # 查询用户信息
    try:
        user = User.query.filter_by(id=g.user_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return R.err(RET.DBERR, '数据库异常')

    if name is not None:
        user.name = name

    if mobile is not None:
        user.mobile = mobile

    if avatar_url is not None:
        user.avatar_url = avatar_url

    try:
        db_.session.commit()
    except IntegrityError as e:
        # 数据库操作失败后回滚
        db_.session.rollback()
        # 表示出现重复值
        current_app.logger.error(e)
        return R.err(RET.DATAEXIST, '用户以存在')
    except Exception as e:
        # 数据库操作失败后回滚
        db_.session.rollback()
        current_app.logger.error(e)
        return R.err(RET.DBERR, '数据库异常')

    return R.ok('修改成功')


@api.route('/user/delete', methods=['POST'])
def delete():
    """
    删除用户
    参数格式： JSON
    :return:
    """

    # 获取前端JSON数据，返回字典
    req_dict = request.get_json()

    user_id = req_dict.get('user_id')

    # 查询用户信息
    try:
        user = User.query.filter_by(id=user_id).first()
        db_.session.delete(user)
        db_.session.commit()
    except Exception as e:
        # 数据库操作失败后回滚
        db_.session.rollback()
        current_app.logger.error(e)
        return R.err(RET.DBERR, '数据库异常')

    return R.ok('删除成功')


@api.route('/user/avatar', methods=['POST'])
def set_user_avatar():
    """
    设置用户头像
    参数： 图片（多媒体表单）， 用户Iid
    :return:
    """
    image_file = request.files.get('avatar')

    if image_file is None:
        return R.err(RET.PARAMERR, '未上传图片')

    file_path = '/static/upload/' + secure_filename(image_file.filename)
    file_save_path = 'base' + file_path

    print(file_save_path)

    try:
        image_file.save(file_save_path)
    except Exception as e:
        current_app.logger.error(e)
        return R.err(RET.DATAERR, '保存图片文件失败')

    try:
        User.query.filter_by(id=g.user_id).update({'avatar_url': file_path})
        db_.session.commit()
    except Exception as e:
        db_.session.rollback()
        current_app.logger.error(e)
        return R.err(RET.DBERR, '保存图片信息失败')

    return R.ok('保存成功', {'avatar_url': file_path})
