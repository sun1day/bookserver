"""
@project: bookserver
@Name: book.py
@Auth: Rrsgdl
@Date: 2024/12/19-9:43
"""
import sys

from apps.db_models.base import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy import BIGINT, VARCHAR, Index, UniqueConstraint


class Books(Base):
    """书籍"""
    id = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    hash_value = mapped_column(VARCHAR(32), unique=True, nullable=False)
    # __table_args__ = (Index("idx_account", "account", unique=True),)  # 创建唯一索引


class UserRelateBooks(Base):
    """用户和书籍列表"""
    id = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    book_id = mapped_column(BIGINT)
    book_name = mapped_column(VARCHAR(128))
    user_id = mapped_column(BIGINT)

    __table_args__ = (
        UniqueConstraint(user_id, book_id, name="uq_idx_user_book"),
    )
