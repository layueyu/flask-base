"""
分页
"""

from flask import current_app


class Page:
    """
    分页
    """
    def __init__(self):
        self.__page = 1   # 当前页
        self.__limit = 10  # 每页大小
        self.__total_page = 10  # 总页数
        self.__total_count = 0  # 总记录数
        self.__list = []

    @property
    def page(self):
        return self.__page

    @page.setter
    def page(self, value):
        try:
            self.__page = int(value)
        except Exception as e:
            current_app.logger.error(e)

    @property
    def limit(self):
        return self.__limit

    @limit.setter
    def limit(self, value):
        try:
            self.__limit = int(value)
        except Exception as e:
            current_app.logger.error(e)

    @property
    def total_page(self):
        return self.__total_page

    @total_page.setter
    def total_page(self, value):
        self.__total_page = value

    @property
    def total_count(self):
        return self.__total_count

    @total_count.setter
    def total_count(self, value):
        self.__total_count = value

    @property
    def list(self):
        return self.__list

    @list.setter
    def list(self, value):
        self.__list = value

    def to_dict(self):
        return {
            'page': self.page,
            'limit': self.limit,
            'total_count': self.total_count,
            'total_page': self.total_page,
            'list': self.list
        }
