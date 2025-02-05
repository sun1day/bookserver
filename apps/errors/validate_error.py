"""
@project: bookserver
@Name: field_validate_error.py
@Auth: Rrsgdl
@Date: 2025/2/5-15:38
"""
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from apps.lib.response import FailResponse


class FieldValidateError:
    def __init__(self, code=None):
        self.code = code

    def __call__(self, request: Request, errors: RequestValidationError):
        error_msg = ""
        for error in errors.errors():
            error_msg += ".".join(error.get("loc")) + ":" + error.get("msg") + ";"
        return FailResponse(code=self.code, error_msg=error_msg)
