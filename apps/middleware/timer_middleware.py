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
        params = {
            'query_params': request.query_params,
            'path_params': request.path_params,
        }
        logger.info(f'begin request, url: {request.url}')
        try:
            return await call_next(request)
        except Exception:
            raise
        finally:
            logger.info(f'end request {request.url} cost: {time.monotonic() - start_time}s ')
