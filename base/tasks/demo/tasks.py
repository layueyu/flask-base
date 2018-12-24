"""
发送短信
"""

from base.tasks.main import celery_app


@celery_app.task
def demo():
    """ 异步任务 demo"""
    print('无参异步任务')


@celery_app.task
def demo1(value):
    """ 异步任务 demo"""
    print('有参异步任务，参数: value={}'.format(value))


@celery_app.task
def demo2():
    """ 异步任务 demo"""
    print('带返回值异步任务')
    return '带返回值异步任务，返回数据'

