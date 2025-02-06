"""
@project: bookserver
@Name: dependencies.py
@Auth: Rrsgdl
@Date: 2024/10/15-14:18
"""

# dependencies
import functools

from sqlalchemy.orm import Session

from apps.db.mysql import LocalSession, LocalAsyncSession
from settings.settings import Settings, get_settings
from typing import Annotated
from fastapi import Request, Depends
from apps.db_models.user import User
from apps.service.security import Security
from apps.lib.exceptions.exception import UserNotExistedException


def get_session():
    with LocalSession() as session:
        try:
            yield session
        except Exception:
            session.rollback()
            raise


def get_async_session():
    with LocalAsyncSession() as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
SettingsDep = Annotated[Settings, Depends(get_settings)]


def parse_token(request: Request, conf: SettingsDep):
    token = request.headers.get("token")
    return Security.decode(conf.JwtSecret, token)


def current_user(session: SessionDep, payload=Depends(parse_token)):
    user_id = payload["id"]
    user = session.get(User, user_id)
    if not user:
        raise UserNotExistedException()
    return user


# 需要登录
login_required = current_user

# 获取当前用户
CurrentUserDep = Annotated[User, Depends(current_user)]
