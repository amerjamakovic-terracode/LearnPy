# As far as I understand we have this config file to take redundancy as low as we can,
# dbURL is just there to load it to my db session,
# other stuff is made for tokens and is a subject to study for now
# model config is there to tell pydantic how to load values and teach it how to read the env file

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
