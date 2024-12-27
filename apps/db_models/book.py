"""
@project: bookserver
@Name: book.py
@Auth: Rrsgdl
@Date: 2024/12/19-9:43
"""

from .base import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy import BIGINT, VARCHAR


class Books(Base):
    id = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    hash_value = mapped_column(VARCHAR(32), unique=True, nullable=False)
    # __table_args__ = (Index("idx_account", "account", unique=True),)  # 创建唯一索引


class UserRelateBooks(Base):
    id = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    book_id = mapped_column(BIGINT, index=True)
    book_name = mapped_column(VARCHAR(128))
    user_id = mapped_column(BIGINT, index=True)
