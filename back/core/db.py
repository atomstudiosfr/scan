import logging
import time
from typing import Annotated

import sqlalchemy
from fastapi import Depends
from sqlalchemy import event, NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from core.config import SETTINGS

ASYNC_ENGINE = create_async_engine(SETTINGS.ASYNC_SQLALCHEMY_DATABASE_URI, pool_recycle=3600, pool_size=45)
ASYNC_LOCAL_SESSION = async_sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=ASYNC_ENGINE)

ASYNC_WORKER_ENGINE = create_async_engine(SETTINGS.ASYNC_SQLALCHEMY_DATABASE_URI, poolclass=NullPool)
ASYNC_WORKER_SESSION = async_sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=ASYNC_WORKER_ENGINE)

log_sqltime = logging.getLogger("sqltime")


async def get_db_worker():
    async with ASYNC_WORKER_SESSION() as db:
        return db


async def get_db():
    try:
        async with ASYNC_LOCAL_SESSION() as db:
            yield db
    finally:
        await db.aclose()


dbDep = Annotated[AsyncSession, Depends(get_db)]


@event.listens_for(sqlalchemy.engine.Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault("query_start_time", []).append(time.time())
    log_sqltime.debug("Start Query: %s", statement)


@event.listens_for(sqlalchemy.engine.Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info["query_start_time"].pop(-1)
    log_sqltime.debug("Query Complete => Total Time: %f", total)
