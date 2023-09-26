import fastapi

from core.build import AppBuilder


class AppFactory:
    """Application factory to generate
    fully bundled fastapi application

    Returns:
        object: fastapi instance
    """

    @staticmethod
    def initialize_app() -> fastapi.FastAPI:
        app_instance = AppBuilder()
        return app_instance.build_app()
