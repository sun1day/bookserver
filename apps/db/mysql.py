"""
@project: bookserver
@Name: base.py
@Auth: Rrsgdl
@Date: 2025/2/5-10:59
"""

from sqlalchemy import create_engine, pool, URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from settings.settings import get_settings

settings = get_settings()
engine = create_engine(
    URL.create(**settings.SqlalchemyUrlSettings),
    poolclass=pool.QueuePool,
    **settings.SqlalchemyPoolSettings,
    echo=settings.Debug,
    insertmanyvalues_page_size=500,
)

# 异步engine
async_engine = create_async_engine(
    URL.create(**settings.AsyncSqlalchemyUrlSettings),
    poolclass=pool.AsyncAdaptedQueuePool,
    **settings.SqlalchemyPoolSettings,
    echo=settings.Debug,
    insertmanyvalues_page_size=500,
)

LocalSession = sessionmaker(
    engine, autoflush=False, autocommit=False, expire_on_commit=False
)

LocalAsyncSession = async_sessionmaker(
    async_engine, autoflush=False, autocommit=False, expire_on_commit=False
)
