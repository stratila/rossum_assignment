from pydantic_settings import BaseSettings
from pydantic import (
    Field,
    EmailStr,
)


class Settings(BaseSettings):
    username: str = Field(alias="basic_auth_username")
    password: str = Field(alias="basic_auth_password")
    rossum_api_email: EmailStr = Field()
    rossum_api_password: str = Field()
    rossum_api_custom_domain: str = Field()


settings = Settings()
