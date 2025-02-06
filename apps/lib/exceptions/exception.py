"""
@project: bookserver
@Name: error.py
@Auth: Rrsgdl
@Date: 2024/12/24-17:50
"""
from .base import ServiceBaseException

"""登录校验错误"""


class InvalidTokenException(ServiceBaseException):
    code = 4001
    msg = "请重新登录"


class UserRequestErrorException(ServiceBaseException):
    code = 4000
    msg = "用户请求错误"


class UserNotExistedException(UserRequestErrorException):
    msg = "用户不存在"
