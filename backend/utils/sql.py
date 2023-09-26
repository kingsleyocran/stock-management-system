from typing import Any

from sqlalchemy.orm import Session


def add_item_to_db(db: Session, item: Any) -> bool:
    """
    Add an item to the database
    Args:
        db (object): contain the session for the
                database operations
        item(Any): The item to insert
    returns:
        bool
    """
    db.add(item)
    db.commit()
    db.refresh(item)
    return True


def delete_item_from_db(db: Session, item: Any) -> bool:
    """
    Delete an item to the database
    Args:
        db (object): contain the session for the
                database operations
        item(Any): The item to delete
    returns:
        bool
    """
    db.delete(item)
    db.commit()
    return True
