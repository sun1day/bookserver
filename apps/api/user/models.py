"""
@project: bookserver
@Name: models.py
@Auth: Rrsgdl
@Date: 2024/12/17-17:57
"""

from pydantic import BaseModel


class UserLoginModel(BaseModel):
    username: str
    password: str
