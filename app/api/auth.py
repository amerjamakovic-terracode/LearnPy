from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.db.session import get_db  # handles query's with async db
from app.schemas.user import UserCreate, UserRead
from app.crud import user as crud_user
from app.core.security import create_access_token
from app.core.config import settings  # .env stuff again
from passlib.context import CryptContext  # hashing stuff


router = APIRouter(prefix="/auth", tags=["auth"])
# "/auth" means all endpoints start with /auth
# ["auth"] says to OpenAPI docs to group endpoints

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# deprecated="auto": warning for outdated algorithms in future?

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
# tokenUrl is fastapi endpoint


async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await crud_user.get_user_by_email(db, email=email)
    if not user:
        return None

    if not pwd_context.verify(password, user.password):
        return None

    return user


# check the user first with email than the password and if something is not correct return none if it is correct return the user


@router.post("/register", response_model=UserRead)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):

    existing_user = await crud_user.get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    user = await crud_user.create_user(
        db=db,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        email=user_in.email,
        password=user_in.password,  # Will be hashed in CRUD function
    )
    return user


# Email should be unique so we check if it already exists, if not we generate a new user, hash password in crud and return user


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    """
    Endpoint to log in a user using OAuth2 password flow.
    Returns an access token if credentials are valid.
    Not really sure how exactly this all works so far so this is a topic to discuss
    """
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": user.email},  # 'sub' claim stores the user's email
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await crud_user.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception

    return user


@router.get("/me", response_model=UserRead)
async def read_users_me(current_user=Depends(get_current_user)):
    """
    Returns info about the current logged-in user.
    Uses get_current_user dependency to ensure the request is authenticated.
    """
    return current_user
