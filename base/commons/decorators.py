"""
装饰器
"""
import functools


def decorator_demo(func):
    """装饰器 demo"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 业务处理
        return func(*args, **kwargs)
    return wrapper
