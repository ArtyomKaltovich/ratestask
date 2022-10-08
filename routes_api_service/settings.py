from pydantic import BaseSettings


class Settings(BaseSettings):
    dbname: str = "postgres"
    user: str = "postgres"
    password: str = "ratestask"
    host: str = "192.168.56.101"
    port: int = 5432
    debug: bool = False
