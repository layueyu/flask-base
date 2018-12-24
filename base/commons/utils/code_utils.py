"""
编码 模块
"""

import hashlib


def hl_sha256(key, value):
    """
    sha256 加密
    :return: 加密结果转成16进制字符串形式，并大写
    """
    _hs_sha256 = hashlib.sha256(key.encode("utf-8"))
    _hs_sha256.update(value.encode("utf-8"))
    return _hs_sha256.hexdigest()


def hl_md5(key, value):
    """
    md5 加密
    :return: 加密结果转成16进制字符串形式，并大写
    """
    _hs_sha256 = hashlib.md5(key.encode("utf-8"))
    _hs_sha256.update(value.encode("utf-8"))
    return _hs_sha256.hexdigest()
