"""
@project: bookserver
@Name: view.py
@Auth: Rrsgdl
@Date: 2024/10/15-14:33
"""
import time

from fastapi import APIRouter
from fastapi import applications, Depends
from fastapi import Body
from .models import UserLoginModel
from apps.service.security import Security
from sqlalchemy.orm import Session
from typing import Annotated
from apps.dependencies import SessionDep, SettingsDep
from apps.models.user import User
from ...lib.exceptions.exception import UserNotExistedException

user_router = APIRouter(prefix="/user")


@user_router.post("/login")
def login(login_model: UserLoginModel, session: SessionDep, settings: SettingsDep):
    user = (
        session.query(User)
        .filter_by(account=login_model.account, password=login_model.password)
        .first()
    )
    if not user:
        raise UserNotExistedException()

    if user.is_deleted():
        raise UserNotExistedException()

    payload = {'id': user.id, 'account': user.account, 'timestamp': int(time.time())}
    token = Security.create_token(settings.JwtSecret, payload, expire=settings.TokenExpire)
    return
