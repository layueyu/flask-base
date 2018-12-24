"""
自定以转换器-模块
"""

from werkzeug.routing import BaseConverter


class ReConverter(BaseConverter):
    """
    定义正则转换器
    """
    def __init__(self, url_map, regex):
        # 调用父类初始化方法
        super(ReConverter, self).__init__(url_map)
        self.regex = regex


class MobileConverter(BaseConverter):
    """
    定义正则转换器
    """
    def __init__(self, url_map):
        # 调用父类初始化方法
        super(ReConverter, self).__init__(url_map)
        self.regex = r'1[345678]\d{9}'
