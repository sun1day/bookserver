"""
@project: bookserver
@Name: app.py
@Auth: Rrsgdl
@Date: 2024/10/15-14:18
"""

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from apps.errors.validate_error import FieldValidateError
from apps.middleware.exception_middleware import ExceptionMiddleware
from apps.middleware.timer_middleware import TimerMiddleware
from uvicorn.loops import auto
from settings.settings import Settings
from fastapi.exceptions import RequestValidationError
from logging import getLogger, StreamHandler, Formatter
from logging.handlers import TimedRotatingFileHandler


def create_app():
    app = FastAPI(docs_url=Settings.OpenDocsUrl, openapi_url=None, openapi_tags=None)
    app.state.settings = Settings
    config_logger(app)
    register_router(app)
    register_middleware(app)
    auto.auto_loop_setup()
    register_exception(app)
    return app


def register_router(app: FastAPI):
    """注册路由"""
    from apps.api.router import create_router

    app.include_router(create_router(), prefix="/v1/api")
    # for r in app.routes:
    #     print(r.path)
    return


def register_middleware(app: FastAPI):
    # 错误处理和时间需要在最后
    app.add_middleware(ExceptionMiddleware)
    app.add_middleware(TimerMiddleware)
    app.add_middleware(
        CORSMiddleware,  # noqa
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register_exception(app: FastAPI):
    # 参数校验错误
    app.add_exception_handler(RequestValidationError, FieldValidateError())


def config_logger(app: FastAPI):
    setting: Settings = app.state.settings
    root = getLogger()
    # 设置根记录器日志级别
    root.setLevel(setting.LoggerLevel)

    # 格式化器
    formatter = Formatter(
        "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s"
    )

    file_hdl = TimedRotatingFileHandler(
        setting.LoggerFile, when=setting.When, backupCount=setting.BackupCount
    )
    stream_hdl = StreamHandler()
    file_hdl.setLevel(setting.LoggerLevel)
    stream_hdl.setLevel(setting.LoggerLevel)
    file_hdl.setFormatter(formatter)
    stream_hdl.setFormatter(formatter)
    root.addHandler(stream_hdl)
    root.addHandler(file_hdl)
    return
