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
    """
    定时任务 返回数据
     - 通过get方法能获取celery异步执行结果
     - get 方法默认是阻塞的行为， 会等到有了执行结果子后才返回
     - get 方法也接受参数timeout， 超时时间， 超时后立即返回
    """
    result = demo2.delay()

    data = {
        'id': result.id,
        'data': result.get(),
    }

    return R.ok('OK', data)
