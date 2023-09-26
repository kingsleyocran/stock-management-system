"""General Application Settings

This module stores all the configurations
for the application
"""
import pydantic
from sqlalchemy_imageattach.stores.fs import HttpExposedFileSystemStore
from sqlalchemy_imageattach.stores.s3 import S3Store


class AppSettings(pydantic.BaseSettings):
    """Application Settings"""

    DATABASE_URL: str
    TEST_DATABASE_URL: str
    TESTING: bool
    LOG_FILENAME: str = "application.log"
    API_PREFIX: str = "/api/v1"
    APP_TITLE: str = "API Store"
    APP_DESCRIPTION: str = "API for managing stores"
    IMAGE_STORAGE_PATH_PREFIX: str = "images"
    SERVER_NAME: str = "http://localhost:8000"
    FRONTEND_URL: str = "http://localhost:3000"
    AWS_BUCKET: str = "store-api-bucket"
    AWS_ACCESS_KEY: str = "XXXXXXXXXXXXXXXXXXXX"
    AWS_SECRET_KEY: str = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    AWS_SERVER_NAME: str = "http://localhost:8000"
    authjwt_access_token_expires: int = 15
    authjwt_refresh_token_expires: int = 1440
    authjwt_secret_key: str = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

    class Config:
        """Meta configuration"""

        env_file = ".env"


class FileStorage:
    def __init__(self) -> None:
        self.settings = AppSettings()
        self.profile_store = HttpExposedFileSystemStore(
            path=f"{self.settings.IMAGE_STORAGE_PATH_PREFIX}/user_images",
            prefix="/profile",
            host_url_getter=lambda: self.settings.SERVER_NAME,
        )
        self.product_store = HttpExposedFileSystemStore(
            path=f"{self.settings.IMAGE_STORAGE_PATH_PREFIX}/product_images",
            prefix="/product",
            host_url_getter=lambda: self.settings.SERVER_NAME,
        )

    def get_profile_store(self) -> HttpExposedFileSystemStore:
        return self.profile_store

    def get_product_store(self) -> HttpExposedFileSystemStore:
        return self.product_store


class AwsStorage:
    def __init__(self) -> None:
        self.settings = AppSettings()
        self.profile_store = S3Store(
            bucket=self.settings.AWS_BUCKET,
            access_key=self.settings.AWS_ACCESS_KEY,
            secret_key=self.settings.AWS_SECRET_KEY,
            prefix="/profile",
            public_base_url=self.settings.SERVER_NAME,
        )
        self.product_store = S3Store(
            bucket=self.settings.AWS_BUCKET,
            access_key=self.settings.AWS_ACCESS_KEY,
            secret_key=self.settings.AWS_SECRET_KEY,
            prefix="/product",
            public_base_url=self.settings.AWS_SERVER_NAME,
        )

    def get_profile_store(self) -> S3Store:
        return self.profile_store

    def get_product_store(self) -> S3Store:
        return self.product_store


class EmailSettings(pydantic.BaseSettings):
    """Email Settings"""

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_SSL_TLS: bool = True
    MAIL_DEBUG: bool = False
    USE_CREDENTIALS: bool = True
    MAIL_STARTTLS: bool = False
    VALIDATE_CERTS = True
    TEMPLATE_FOLDER: str = "templates"

    class Config:
        """Meta configuration"""

        env_file = ".env"
