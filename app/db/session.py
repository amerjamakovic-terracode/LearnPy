from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings  # make it use config class to load url

DATABASE_URL = settings.DATABASE_URL  # Load DB url from .env

# Create async engine and connect it to postgess db
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a session factory
SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine,  # how to connect
    class_=AsyncSession,  # make each session async bc fastapi endpoints
    expire_on_commit=False,  # keep object usable after commit
)


# automaticly open nad close sessions while interacting with api
async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
