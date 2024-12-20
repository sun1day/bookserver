"""
@project: bookserver
@Name: view.py
@Auth: Rrsgdl
@Date: 2024/10/15-14:33
"""

from fastapi import APIRouter
from fastapi import applications
from fastapi import Body
from .models import UserLoginModel

user_router = APIRouter(prefix="/user")


@user_router.post("/login")
def login(login_item: UserLoginModel):
    return {
        "code": 1,
        "data": {"token": f"Token: {login_item.username}-{login_item.password}"},
        "err_msg": "",
    }
