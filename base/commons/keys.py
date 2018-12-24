"""
自定以 KEY
"""


class RedisKeys:
    """
    redis KEY
    """

    @classmethod
    def image_code_key(cls, uuid):
        """图片验证码 KEY"""
        return 'image_code_{}'.format(uuid)

    @classmethod
    def access_err_num_key(cls, ip):
        """ 登录错误 次数 记录"""
        return 'access_err_num_{}'.format(ip)

    @classmethod
    def sms_code_key(cls, mobile):
        """短信验证码 KEY"""
        return 'sms_code_{}'.format(mobile)

    @classmethod
    def send_sms_code_key(cls, mobile):
        """发送 短信验证码 记录 KEY"""
        return 'send_sms_code_{}'.format(mobile)

    @classmethod
    def token_key(cls, user_id):
        """token key"""
        return 'user_token_{}'.format(user_id)
