# database logic layer that sits in between models and api endpoints

from sqlalchemy.future import select  # async friendly query builder
from sqlalchemy.ext.asyncio import AsyncSession  # just a session for db
from app.models.user import User  # user from model
from passlib.context import CryptContext  # hashing for password

pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)  # creating a context for password hashing


# method for returning a hashed password
def hash_password(password: str) -> str:
    return pwd_context.hash(password.encode("utf-8")[:72])


async def create_user(db: AsyncSession, first_name, last_name, email, password):
    # creating user in memory
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=hash_password(password),
    )
    # prepare for adding it to the db
    db.add(user)
    # write the user in db
    await db.commit()
    # id is generated on auto so this makes sure it can read it after
    await db.refresh(user)
    # return it for the api endpoint
    return user


# returns null if user not found and failsafe will be added in api
async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()
