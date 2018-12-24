"""
基类
"""

from datetime import datetime
from base import db_


class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""

    # 记录创建时间
    create_time = db_.Column(db_.DateTime, default=datetime.now)
    # 记录更新时间
    update_time = db_.Column(db_.DateTime, default=datetime.now, onupdate=datetime.now)
