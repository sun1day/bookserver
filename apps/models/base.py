"""
@project: bookserver
@Name: base.py
@Auth: Rrsgdl
@Date: 2024/12/18-17:40
"""
import datetime as dt
from datetime import datetime

from sqlalchemy import create_engine, URL, pool, DATETIME, func, BIGINT, MetaData
from apps.dependencies import get_settings
from sqlalchemy.orm import DeclarativeBase, mapped_column, declared_attr
from apps.utils.util import hump2underline

settings = get_settings()
engine = create_engine(
    URL(**settings.SqlalchemyUrlSettings),
    poolclass=pool.QueuePool,
    **settings.SqlalchemyPoolSettings,
    echo=settings.Debug
)

# 索引命名映射
constraint_naming_conventions = {
    "ix": "ix_%(column_0_N_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class ClsTableMiXin:
    @declared_attr
    def __tablename__(self):
        model_name = type(self).__name__
        return hump2underline(model_name)


class Base(ClsTableMiXin, DeclarativeBase):
    __abstract__ = True
    metadata = MetaData(naming_convention=constraint_naming_conventions)

    status = mapped_column(BIGINT, nullable=False, comment="0: 删除. 1: 正常")
    create_time = mapped_column(
        DATETIME(timezone=True),
        default_factory=datetime.utcnow,
        nullable=False,
        comment="创建时间",
    )
    update_time = mapped_column(
        DATETIME(timezone=True),
        default_factory=datetime.utcnow,
        server_onupdate=func.now(),
    )
