"""
异步任务 worker 配置
"""

# 名称
NAME = 'base'


class Config:
    """
    配置
    """
    # BROKER
    BROKER_URL = 'redis://127.0.0.1:6379/15'

    # BACKEND
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/13'

