"""
demo
"""

from . import api
from base.tasks.demo.tasks import demo, demo1, demo2
from base.commons.response import R


@api.route('/task/test')
def task():
    """无参数定时任务"""
    demo.delay()
    return R.ok('OK')


@api.route('/task/test1')
def task():
    """无参数定时任务"""
    demo1.delay('/task/test1')
    return R.ok('OK')


@api.route('/task/test1')
def task():
    """无参数定时任务"""
    result = demo.delay()
    return R.ok('OK', result)

