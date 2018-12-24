"""
自定以 response 返回值 - 模块
"""
from flask import jsonify


class RET:
    """
    返回值 code
    """
    OK = "0"
    DBERR = "4001"
    NODATA = "4002"
    DATAEXIST = "4003"
    DATAERR = "4004"
    SESSIONERR = "4101"
    LOGINERR = "4102"
    PARAMERR = "4103"
    USERERR = "4104"
    ROLEERR = "4105"
    PWDERR = "4106"
    TOKENINVALID = "4107"
    REQERR = "4201"
    IPERR = "4202"
    THIRDERR = "4301"
    IOERR = "4302"
    SERVERERR = "4500"
    UNKOWNERR = "4501"


# 返回值 code 对应关系
error_map = {
    RET.OK: "成功",
    RET.DBERR: "数据库查询错误",
    RET.NODATA: "无数据",
    RET.DATAEXIST: "数据已存在",
    RET.DATAERR: "数据错误",
    RET.SESSIONERR: "用户未登录",
    RET.LOGINERR: "用户登录失败",
    RET.PARAMERR: "参数错误",
    RET.USERERR: "用户不存在或未激活",
    RET.ROLEERR: "用户身份错误",
    RET.PWDERR: "密码错误",
    RET.TOKENINVALID: "token 失效",
    RET.REQERR: "非法请求或请求次数受限",
    RET.IPERR: "IP受限",
    RET.THIRDERR: "第三方系统错误",
    RET.IOERR: "文件读写错误",
    RET.SERVERERR: "内部错误",
    RET.UNKOWNERR: "未知错误",
}


class ResultKey:
    """
    视图 返回值 KEY
    """
    CODE_KEY = 'code'
    MSG_KEY = 'msg'
    DATA_KEY = 'data'


class R(object):
    """
    通用 返回值 R
    """

    @classmethod
    def result_json(cls, code, msg, data):
        """
        按 json 格式返回数据
        :param code: 返回值代码
        :param msg:  消息
        :param data: 数据
        :return:
        """
        _result = {}

        _result[ResultKey.CODE_KEY] = code
        _result[ResultKey.MSG_KEY] = msg
        if data is None:
            _result[ResultKey.DATA_KEY] = data

        return jsonify(_result)

    @classmethod
    def err(cls, code, msg=''):
        return cls.result_json(code=code, msg=msg, data=None)

    @classmethod
    def ok(cls, msg=''):
        return cls.result_json(code=RET.OK, msg=msg, data=None)

    @classmethod
    def ok(cls, msg, data):
        return cls.result_json(code=RET.OK, msg=msg, data=data)

