import os
from typing import Union

import fastapi
from fastapi.exceptions import RequestValidationError, ValidationError
from fastapi.staticfiles import StaticFiles
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.exc import DBAPIError, IntegrityError
from fastapi.middleware.cors import CORSMiddleware

from api.v1.router import accounts, orders, products, users
from config import setting
from core import setup as db_setup
from handlers import exceptions as exc
from fastapi_pagination import add_pagination
from fastapi_pagination.utils import disable_installed_extensions_check


disable_installed_extensions_check()
settings = setting.AppSettings()


class AppSingleton:
    """Application Instance creation

    This class instantiate an application
    only once.
    Attributes:
        _app_instance (object, None): Application instance

    """

    _app_instance = None

    @classmethod
    def get_app_instance(cls) -> Union[fastapi.FastAPI, None]:
        """Instantiate a fastapi application

        This method generates a fastapi application
        instance

        Returns:
            object: fastapi application instance
        """
        if cls._app_instance is None:
            cls._app_instance = fastapi.FastAPI()
        return cls._app_instance


class AppBuilder:
    def __init__(self):
        self._app = AppSingleton.get_app_instance()

    def register_database(self) -> None:
        """Register all databases"""
        db_setup.Base.metadata.create_all(
            bind=db_setup.database.get_engine  # type : ignore
        )

    def add_app_details(
        self, title: str = None, description: str = None  # type: ignore
    ) -> None:
        """Append features to the fastapi instance

        This method is responsible for including
        details to the fastapi instance

        Args:
            title (str): Title used for the application
            description (str): Description for the application
        """
        self._app.title = title
        self._app.description = description

    def register_routes(self) -> None:
        """Register routes to be used

        This method is used to handle all
        routers for the application
        """
        self._app.include_router(
            users.router, prefix=settings.API_PREFIX, tags=["Users"]
        )
        self._app.include_router(
            accounts.router, prefix=settings.API_PREFIX, tags=["Accounts"]
        )

        self._app.include_router(
            products.router, prefix=settings.API_PREFIX, tags=["Products"]
        )

        self._app.include_router(
            orders.router, prefix=settings.API_PREFIX, tags=["Orders"]
        )

        @self._app.get("/", include_in_schema=False)
        def _index() -> fastapi.responses.RedirectResponse:
            """Redirect visitor to the docs page

            Returns:
                object: redirect response
            """
            return fastapi.responses.RedirectResponse("/docs")

    def register_exceptions(self) -> None:
        self._app.add_exception_handler(ValidationError, exc.validation_error_handler)
        self._app.add_exception_handler(
            RequestValidationError, exc.validation_error_handler
        )

        self._app.add_exception_handler(DBAPIError, exc.db_error_handler)
        self._app.add_exception_handler(IntegrityError, exc.db_error_handler)

        self._app.add_exception_handler(ValueError, exc.value_error_handler)
        self._app.add_exception_handler(AuthJWTException, exc.auth_error_handler)

    def register_storages(self):
        """Register storages

        This method is used to register
        all storages for the application

        Args:
            storage (object): Storage instance
        """
        self._app.mount(
            "/product",
            StaticFiles(
                directory=f"{settings.IMAGE_STORAGE_PATH_PREFIX}/product_images"
            ),
        )
        self._app.mount(
            "/profile",
            StaticFiles(directory=f"{settings.IMAGE_STORAGE_PATH_PREFIX}/user_images"),
        )

    def register_middleware(self):
        self._app.add_middleware(CORSMiddleware,
                                 allow_origins=[
                                     "*"],
                                 allow_credentials=True,
                                 allow_methods=["*"],
                                 allow_headers=["*"])

    def create_folders(self) -> None:
        """Create folders

        This method is used to create
        all folders for the application
        """
        os.makedirs(settings.IMAGE_STORAGE_PATH_PREFIX, exist_ok=True)
        os.makedirs(settings.IMAGE_STORAGE_PATH_PREFIX + "/user_images", exist_ok=True)
        os.makedirs(
            settings.IMAGE_STORAGE_PATH_PREFIX + "/product_images", exist_ok=True
        )

    def build_app(self) -> fastapi.FastAPI:
        """Build Application

        This method is used to construct the
        application

        Returns:
            object: fastapi instance
        """
        self.create_folders()
        self.register_database()
        self.add_app_details(
            title=settings.APP_TITLE,
            description=settings.APP_DESCRIPTION,
        )
        self.register_exceptions()
        self.register_routes()
        self.register_storages()
        # self.register_middleware()
        add_pagination(self._app)
        return self._app
