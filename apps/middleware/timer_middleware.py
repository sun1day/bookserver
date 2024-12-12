"""
@project: bookserver
@Name: timer.py
@Auth: Rrsgdl
@Date: 2024/12/12-17:03
"""
import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class TimerMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:

        start_time = time.monotonic()
        try:
            return await call_next(request)
        except Exception:
            raise
        finally:
            logger.info(f'{request.url} cost{time.monotonic() - start_time}s ')
