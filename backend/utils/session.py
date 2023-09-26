"""Session
Context manager to maintain the
session of a database
"""

from typing import Generator

from core import setup


def create() -> Generator:
    """Create a session for the database
    operation

    Yields:
        object: database session
    """
    try:
        db_init = setup.DatabaseSetup()
        db = db_init.get_session()
        yield db()

    finally:
        db().close()
