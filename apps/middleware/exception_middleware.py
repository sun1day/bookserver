"""
@project: bookserver
@Name: exception_middleware.py
@Auth: Rrsgdl
@Date: 2024/12/26-16:45
"""

import time
import logging
import traceback

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from apps.lib.exceptions.base import ServiceBaseException
from apps.lib.exceptions.exception import InvalidTokenException
from apps.lib.response import FailResponse

logger = logging.getLogger(__name__)


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            return await call_next(request)
        except InvalidTokenException as e:
            return FailResponse(error_msg=e.msg)
        except ServiceBaseException as e:
            return FailResponse(code=e.code, error_msg=e.msg)
        except Exception:
            logger.error(f'path: {request.url}. error: {traceback.format_exc()}')
            return FailResponse(error_msg='System error')
