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
from .models import UserLoginModel, UserResetPassword
from apps.service.security import Security
from sqlalchemy.orm import Session
from typing import Annotated
from apps.dependencies import SessionDep, SettingsDep, CurrentUserDep
from apps.db_models.user import User
from apps.lib.exceptions.exception import UserNotExistedException
from apps.lib.response import SuccessResponse, FailResponse

user_router = APIRouter(prefix="/user")


@user_router.post("/login")
def login(login_model: UserLoginModel, session: SessionDep, settings: SettingsDep):
    user = (
        session.query(User)
        .filter_by(account=login_model.account, password=login_model.password)
        .first()
    )
    if not user or user.is_deleted():
        raise UserNotExistedException()

    payload = {"id": user.id, "account": user.account, "timestamp": int(time.time())}
    token = Security.create_token(
        settings.JwtSecret, payload, expire=settings.TokenExpire
    )
    return SuccessResponse(data={"token": token})


@user_router.post("/logout")
def logout(current_user: CurrentUserDep):
    return SuccessResponse()


@user_router.post("/reset_password")
def reset_password(
    current_user: CurrentUserDep, reset_model: UserResetPassword, session: SessionDep
):
    """重置密码"""
    if current_user.password != reset_model.password:
        return FailResponse(error_msg="原密码错误!")

    current_user.password = reset_model.new_password
    session.commit()
    return SuccessResponse()
