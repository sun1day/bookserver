"""
@project: bookserver
@Name: dependencies.py
@Auth: Rrsgdl
@Date: 2024/10/15-14:18
"""

# dependencies
import functools

from sqlalchemy import create_engine, pool, URL, AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import Session, sessionmaker

from settings import settings as config
from typing import Annotated
from fastapi import Request, Depends
from apps.db_models.user import User
from apps.service.security import Security
from apps.lib.exceptions.exception import UserNotExistedException


@functools.lru_cache
def get_settings():
    return config.Settings


settings = get_settings()
engine = create_engine(
    URL.create(**settings.SqlalchemyUrlSettings),
    poolclass=pool.QueuePool,
    **settings.SqlalchemyPoolSettings,
    echo=settings.Debug,
    insertmanyvalues_page_size=500,
)

# 异步engine
async_engine = create_async_engine(
    URL.create(**settings.AsyncSqlalchemyUrlSettings),
    poolclass=pool.AsyncAdaptedQueuePool,
    **settings.SqlalchemyPoolSettings,
    echo=settings.Debug,
    insertmanyvalues_page_size=500,
)

LocalSession = sessionmaker(
    engine, autoflush=False, autocommit=False, expire_on_commit=False
)

LocalAsyncSession = async_sessionmaker(
    async_engine, autoflush=False, autocommit=False, expire_on_commit=False
)


def get_session():
    with LocalSession() as session:
        yield session


def get_async_session():
    with LocalAsyncSession as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
SettingsDep = Annotated[config.Settings, Depends(get_settings)]


def parse_token(request: Request, conf: SettingsDep):
    token = request.headers.get("token")
    return Security.decode(conf.JwtSecret, token)


def current_user(session: SessionDep, payload=Depends(parse_token)):
    user_id = payload["id"]
    user = session.get(User, user_id)
    if not user:
        raise UserNotExistedException()
    return user


CurrentUserDep = Annotated[User, Depends(current_user)]
