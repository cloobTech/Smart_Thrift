from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEV_ENV: str
    ST_DB_HOST: str
    ST_DB_PORT: str
    ST_DB_PWD: str
    ST_DB_NAME: str
    ST_DB_USERNAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"


settings = Settings()
