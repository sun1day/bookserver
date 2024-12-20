"""
@project: bookserver
@Name: user.py
@Auth: Rrsgdl
@Date: 2024/12/19-9:43
"""

from .base import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import BIGINT, VARCHAR, Index


class User(Base):
    id = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    account = mapped_column(VARCHAR(64), nullable=False, index=True, comment="账号")
    password = mapped_column(VARCHAR(256), nullable=False, comment="密码")

    __table_args__ = (Index("idx_account", "account", unique=True),)  # 创建唯一索引

    def __repr__(self):
        return f"<User: {self.account}>"
