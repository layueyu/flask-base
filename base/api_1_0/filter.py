"""
过滤器
"""


class OauthFilter:
    """
    访问路径 权限过滤
    """
    url_filter_maps = [
        ('/static/', 'anon'),
        ('/api/v1.0/login', 'anon'),
        ('/api/v1.0/image_code', 'anon'),
        ('/', 'oauth')
        # ('/', 'anon')
    ]

    @classmethod
    def check_url_oauth(cls, path):
        for re_str, oauth in cls.url_filter_maps:
            if path.startswith(re_str):
                return oauth
        return 'oauth'
