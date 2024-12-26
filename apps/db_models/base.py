"""
@project: bookserver
@Name: base.py
@Auth: Rrsgdl
@Date: 2024/12/18-17:40
"""
import datetime as dt
from datetime import datetime
import typing as t

from sqlalchemy import (
    create_engine,
    URL,
    pool,
    DATETIME,
    func,
    BIGINT,
    MetaData,
    inspect,
)
from apps.dependencies import get_settings
from sqlalchemy.orm import DeclarativeBase, mapped_column, declared_attr, sessionmaker
from apps.utils.util import hump2underline

settings = get_settings()
engine = create_engine(
    URL(**settings.SqlalchemyUrlSettings),
    poolclass=pool.QueuePool,
    **settings.SqlalchemyPoolSettings,
    echo=settings.Debug,
    insertmanyvalues_page_size=500,
)

LocalSession = sessionmaker(
    engine, autoflush=False, autocommit=False, expire_on_commit=False
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
    @declared_attr.directive
    def __tablename__(self):
        model_name = type(self).__name__
        return hump2underline(model_name)

    @classmethod
    def create(cls, **kwargs):
        self = cls()
        for k, v in kwargs:
            if hasattr(self, k):
                setattr(self, k, v)
        return self

    def update(self, **kwargs):
        for key in kwargs.keys():
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
        return self

    def to_dict(self):
        # 返回所有字段字典,日期自动转成可读形式Y-m-d H:M:S
        # 用法 query.to_dict()
        return {d: getattr(self, d) for d in inspect(self).columns.keys()}


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
    delete_time = mapped_column(DATETIME(timezone=True))  # 删除时间

    def soft_delete(self):
        self.status = 0

    def __repr__(self):
        return (
            f"{type(self).__name__}"
            f'({",".join([f"{k}={getattr(self, k)}" for k in self.__table__.columns.keys()])})'
        )

    def is_deleted(self) -> bool:
        return self.status == 0
