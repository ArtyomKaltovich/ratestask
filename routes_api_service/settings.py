from pydantic import BaseSettings


class Settings(BaseSettings):
    dbname: str = "postgres"
    dbuser: str = "postgres"
    dbpassword: str = "ratestask"
    dbhost: str = "192.168.56.101"
    dbport: int = 5432
    api_host: str = "0.0.0.0"
    api_port: int = 8080
    debug: bool = False
