from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import sys
import os
import ssl

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import settings

ssl_ctx                = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode    = ssl.CERT_NONE

engine = create_async_engine(
    settings.database_url,
    echo          = True,
    pool_pre_ping = True,
    pool_recycle  = 1800,
    connect_args  = {"ssl": ssl_ctx}
)

AsyncSessionLocal = sessionmaker(
    bind             = engine,
    class_           = AsyncSession,
    expire_on_commit = False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session