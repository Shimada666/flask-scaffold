from werkzeug.exceptions import HTTPException


# 业务code与http code 从属于不同领域，尽量与http code分开


class APIException(HTTPException):
    code = 10001
    msg = '抱歉，服务器未知错误'

    def __init__(self, code=None, msg=None, headers=None):
        if code:
            self.code = code
        if msg:
            self.msg = msg
        if headers is not None:
            headers_merged = headers.copy()
            headers_merged.update(self.headers)
            self.headers = headers_merged

        super(APIException, self).__init__(msg, None)

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]


class ServicePauseException(APIException):
    code = 10002
    msg = '服务暂停'


class IpBanedException(APIException):
    code = 10003
    msg = 'IP被限制无法请求该资源'


class IllegalArgumentException(APIException):
    code = 10004
    msg = '参数错误'


class RateLimitException(APIException):
    code = 10005
    msg = '任务过多，后端限流'


class TimeoutException(APIException):
    code = 10006
    msg = '超时错误'


class IllegalRequestException(APIException):
    code = 10007
    msg = '不合法的请求'


class IllegalUserException(APIException):
    code = 10008
    msg = '非法用户'


class PermissionDeniedException(APIException):
    code = 1009
    msg = '没有权限'


class TooLargeRequestException(APIException):
    code = 10010
    msg = '请求长度超过限制'


class IllegalAPIException(APIException):
    code = 10011
    msg = '错误的接口'


class IllegalRequestMethodException(APIException):
    code = 10012
    msg = '错误的请求方式'


class APINotFoundException(APIException):
    code = 10013
    msg = '接口未找到'


class FileTooLargeException(APIException):
    code = 11000
    msg = '文件体积过大'


class FileTooManyException(APIException):
    code = 11001
    msg = '文件数量过多'


class FileExtensionException(APIException):
    code = 11002
    msg = '文件扩展名不符合规范'


class AuthFailedException(APIException):
    code = 20000
    msg = '认证错误'
