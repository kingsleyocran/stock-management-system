from datetime import timedelta
from typing import Any

from fastapi import security
from fastapi_jwt_auth import AuthJWT

from config import setting

settings = setting.AppSettings()


@AuthJWT.load_config
def get_config() -> setting.AppSettings:
    settings.authjwt_access_token_expires = timedelta(
        minutes=settings.authjwt_access_token_expires
    )
    settings.authjwt_refresh_token_expires = timedelta(
        minutes=settings.authjwt_refresh_token_expires
    )
    return settings


@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token: Any) -> bool:
    jti = decrypted_token.jti
    return jti in settings.authjwt_denylist_token_jti


AuthController = AuthJWT
bearerschema = security.HTTPBearer()
