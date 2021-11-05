from pydantic import BaseSettings


class Settings(BaseSettings):
    SLEEP_TIME: int = 5

    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    class Config:
        env_file = ".env"


settings = Settings()
