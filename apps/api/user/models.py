"""
@project: bookserver
@Name: models.py
@Auth: Rrsgdl
@Date: 2024/12/17-17:57
"""

from pydantic import BaseModel, Field
from typing import Annotated


class UserLoginModel(BaseModel):
    account: Annotated[str, Field(..., max_length=64, min_length=3)]
    password: Annotated[str, Field(..., max_length=64, min_length=3)]


"""修改密码"""


class UserResetPasswordModel(BaseModel):
    password: Annotated[str, Field(..., max_length=64, min_length=3)]
    new_password: Annotated[str, Field(..., max_length=64, min_length=3, pattern=r'^[A-Za-z0-9_]+$')]
