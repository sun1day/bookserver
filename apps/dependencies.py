"""
@project: bookserver
@Name: dependencies.py
@Auth: Rrsgdl
@Date: 2024/10/15-14:18
"""

# dependencies
import functools

from sqlalchemy.orm import Session

from settings import settings
from typing import Type, Annotated
from fastapi import Request, Depends
from apps.db_models.base import LocalSession, LocalAsyncSession
from apps.db_models.user import User
from fastapi.security import OAuth2PasswordBearer
from apps.service.security import Security
from apps.lib.exceptions.exception import UserNotExistedException


@functools.lru_cache
def get_settings():
    return settings.Settings


def get_session():
    with LocalSession() as session:
        yield session


def get_async_session():
    with LocalAsyncSession as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
SettingsDep = Annotated[settings.Settings, Depends(get_settings)]


def parse_token(request: Request, config: SettingsDep):
    token = request.headers.get("token")
    return Security.decode(config.JwtSecret, token)


def current_user(session: SessionDep, payload: Depends(parse_token)):
    user_id = payload["id"]
    user = session.get(User, user_id)
    if not user:
        raise UserNotExistedException()
    return user


CurrentUserDep = Annotated[User, Depends(current_user)]
