from datetime import (
    datetime,
    timezone,
    timedelta,
)  # datetime-gets current time, timedelta used to add time
from typing import Optional
from jose import jwt  # library used to encode and decode jwt tokens
from app.core.config import settings  # env stuff


# data dict should be something like user email and it will be stored in token
# expires_delta can override default token time
# making copy of the data to make sure I dont fuck it up
# time for token gets put on, and it returns the token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
