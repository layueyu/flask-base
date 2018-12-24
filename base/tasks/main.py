"""
异步任务 worker 启动模块
"""

from celery import Celery
from base.tasks import setting

# 定义Celery对象
celery_app = Celery(setting.NAME)

# 引入配置信息
celery_app.config_from_object(setting.Config)

# 自动搜索任务
celery_app.autodiscover_tasks(['base.tasks.demo'])



