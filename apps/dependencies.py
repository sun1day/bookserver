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
from apps.models.base import LocalSession


@functools.lru_cache
def get_settings():
    return settings.Settings


def get_session():
    with LocalSession() as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
SettingsDep = Annotated[settings.Settings, Depends(get_settings)]
