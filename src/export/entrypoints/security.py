import secrets
from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from export.settings import settings

http_basic_auth = HTTPBasic()


def basic_auth(
    credentials: Annotated[HTTPBasicCredentials, Depends(http_basic_auth)]
) -> str:
    valid_username = secrets.compare_digest(credentials.username, settings.username)
    valid_password = secrets.compare_digest(credentials.password, settings.password)

    if not valid_username or not valid_password:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Wrong credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
