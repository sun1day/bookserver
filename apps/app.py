"""
@project: bookserver
@Name: app.py
@Auth: Rrsgdl
@Date: 2024/10/15-14:18
"""

from fastapi import FastAPI


def create_app():
    app = FastAPI(debug=True)
    app.debug = True
    register_router(app)


    return app


def register_router(app: FastAPI):
    """注册路由"""
    from apps.api.router import create_router
    app.include_router(create_router(), prefix='/v1')
    return
