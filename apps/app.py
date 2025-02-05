"""
@project: bookserver
@Name: app.py
@Auth: Rrsgdl
@Date: 2024/10/15-14:18
"""

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from apps.errors.field_validate_error import FieldValidateError
from apps.middleware.exception_middleware import ExceptionMiddleware
from apps.middleware.timer_middleware import TimerMiddleware
from uvicorn.loops import auto
from settings.settings import Settings
from fastapi.exceptions import RequestValidationError


def create_app():
    app = FastAPI(docs_url=Settings.OpenDocsUrl, openapi_url=None, openapi_tags=None)
    register_router(app)
    register_middleware(app)
    auto.auto_loop_setup()
    register_exception(app)
    return app


def register_router(app: FastAPI):
    """注册路由"""
    from apps.api.router import create_router
    app.include_router(create_router(), prefix='/v1/api')
    # for r in app.routes:
    #     print(r.path)
    return


def register_middleware(app: FastAPI):
    # 错误处理和时间需要在最后
    app.add_middleware(ExceptionMiddleware)
    app.add_middleware(TimerMiddleware)
    app.add_middleware(
        CORSMiddleware,  # noqa
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register_exception(app: FastAPI):

    # 参数校验错误
    app.add_exception_handler(RequestValidationError, FieldValidateError())

