"""
@project: bookserver
@Name: app.py
@Auth: Rrsgdl
@Date: 2024/10/15-14:18
"""

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from apps.middleware.timer_middleware import TimerMiddleware
from uvicorn.loops import auto
from settings.settings import Settings


def create_app():
    app = FastAPI(docs_url=Settings.OpenDocsUrl, openapi_url=None, openapi_tags=None)
    register_router(app)
    register_middleware(app)
    auto.auto_loop_setup()
    return app


def register_router(app: FastAPI):
    """注册路由"""
    from apps.api.router import create_router
    app.include_router(create_router(), prefix='/v1/api')
    return


def register_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,  # noqa
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(TimerMiddleware)
