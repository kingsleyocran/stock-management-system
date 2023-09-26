"""Setup Database for usage

This module shows how to setup and
instantiate a database connection

Attributes:
    settings (object): Application settings
"""
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import setting

settings = setting.AppSettings()


class DatabaseSetup:
    """Database Setup Operator

    This class is responsible for
    performing database setup and
    granting sessions
    """

    def __init__(self) -> None:
        """Construct an Database Operator"""
        if settings.TESTING:
            self._engine = create_engine(
                settings.TEST_DATABASE_URL,  # type: ignore
                connect_args={"check_same_thread": False},
            )
        else:
            self._engine = create_engine(settings.DATABASE_URL)
        self._session_maker = sessionmaker(
            bind=self._engine, autocommit=False, autoflush=False
        )
        self._base = declarative_base()

    def get_session(self) -> sessionmaker:
        """Grant session

            This method returns the database
            session
        Returns:
            object: database session
        """
        return self._session_maker

    @property
    def get_base(self) -> Any:
        """Grant Base

            This method returns the
            database Base
        Returns:
            object: database base
        """
        return self._base

    @property
    def get_engine(self) -> Any:
        """Grant engine
            This method returns the
            database engine

        Returns:
            object: database engine
        """
        return self._engine


database = DatabaseSetup()
Base = database.get_base
