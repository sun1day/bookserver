"""
@project: bookserver
@Name: response.py
@Auth: Rrsgdl
@Date: 2024/12/26-16:28
"""
__all__ = (
    "SuccessResponse",
    "FailResponse",
)

import ujson
from fastapi.responses import Response
from starlette.background import BackgroundTask
import typing as t


class BaseResponse(Response):
    media_type = "application/json"
    status_code: int
    code: int

    def __init__(
        self,
        data: t.Dict = None,
        code: int = None,
        error_msg: str = "",
        headers: t.Mapping[str, str] | None = None,
        background: BackgroundTask | None = None,
    ):
        if code:
            self.code = code
        if data is None:
            data = {}

        content = {"code": self.code, "data": data, "error_msg": error_msg}
        super().__init__(
            content, self.status_code, headers, self.media_type, background
        )

    def render(self, content: t.Any) -> bytes:
        return ujson.dumps(
            content,
            ensure_ascii=False,
        ).encode("utf-8")


class SuccessResponse(BaseResponse):
    status_code = 200
    code = 1


class FailResponse(BaseResponse):
    status_code = 200
    code = 0
