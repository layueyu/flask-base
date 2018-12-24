"""
项目启动文集

获取帮助：
    python manager.py --help

启动服务：
    python manager.py runserver
"""
from base import init

app, manager = init('dev')

if __name__ == '__main__':
    manager.run()
