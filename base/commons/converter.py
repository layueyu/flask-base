"""
自定以转换器-模块
"""

from werkzeug.routing import BaseConverter
from . import regex


class ReConverter(BaseConverter):
    """
    定义正则转换器
    """
    def __init__(self, url_map, regex_):
        # 调用父类初始化方法
        super(ReConverter, self).__init__(url_map)
        self.regex = regex_


class MobileConverter(BaseConverter):
    """
    定义正则转换器
    """
    def __init__(self, url_map):
        # 调用父类初始化方法
        super(MobileConverter, self).__init__(url_map)
        self.regex = regex.MOBILE_RE
