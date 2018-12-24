"""
常量-模块
"""
# 图片验证码的redis有效期, 单位： 妙
IMAGE_CODE_REDIS_EXPIRES = 180

# 短信验证码的redis有效期, 单位： 妙
SMS_CODE_REDIS_EXPIRES = 300

# 发送短信验证码的间隔， 单位：秒
SEND_SMS_CODE_INTERVAL = 60

# 登陆错误尝试次数
LOGIN_ERROR_MAX_TIMES = 5

# 登陆错误限制时间， 单位：秒
LOGIN_ERROR_FORBID_TIME = 600


