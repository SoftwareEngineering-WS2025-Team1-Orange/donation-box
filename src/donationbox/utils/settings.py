from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(".env"))


class Settings(BaseSettings):
    mainframe_socket_url: str
    jwt: str
    passkey: str
    encryption_key: bytes

    model_config = SettingsConfigDict(case_sensitive=False)


settings = Settings()
