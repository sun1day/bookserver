"""
@project: bookserver
@Name: models.py
@Auth: Rrsgdl
@Date: 2024/12/17-17:57
"""

from pydantic import BaseModel, Field
from typing import Annotated


class UserLoginModel(BaseModel):
    account: Annotated[str, Field(..., max_length=64, min_length=8)]
    password: Annotated[str, Field(..., max_length=64, min_length=8)]
