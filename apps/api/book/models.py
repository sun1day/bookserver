"""
@project: bookserver
@Name: models.py
@Auth: Rrsgdl
@Date: 2024/12/17-17:57
"""
from annotated_types import Ge
from pydantic import BaseModel, Field, model_validator, field_validator
from typing import Annotated, TypeVar, Generic, Optional

"""删除书籍"""


class DeleteBookModel(BaseModel):
    book_id: Annotated[int, Field(..., ge=1)]


# 定义一个泛型类型变量
T = TypeVar("T")


# 定义通用响应模型
class ResponseModel(BaseModel, Generic[T]):
    code: int
    message: str
    data: Optional[T] = None

    class Config:
        # 允许使用泛型模型
        arbitrary_types_allowed = True
