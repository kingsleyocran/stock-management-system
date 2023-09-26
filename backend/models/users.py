from datetime import datetime

import sqlalchemy as sq
from sqlalchemy import Enum
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from core import setup
from schemas.enums import Gender, Role


class Users(setup.Base):
    __tablename__ = "users"
    id = sq.Column(sq.Integer, primary_key=True)
    first_name = sq.Column(sq.String, nullable=False)
    last_name = sq.Column(sq.String, nullable=False)
    gender = sq.Column(Enum(Gender), nullable=False)
    role = sq.Column(Enum(Role), nullable=False, default="customer")
    email = sq.Column(sq.String, unique=True, nullable=False)
    hash_password = sq.Column(sq.String, nullable=False)
    orders = relationship("Orders", back_populates="users")
    is_email_verified = sq.Column(sq.Boolean, default=False)
    is_admin = sq.Column(sq.Boolean, default=False)
    joined_at = sq.Column(sq.DateTime, default=datetime.now())
    updated_at = sq.Column(
        sq.DateTime, default=datetime.utcnow(), onupdate=datetime.now()
    )

    @staticmethod
    def set_password(password: str) -> str:
        encrypted_password = generate_password_hash(password)
        return encrypted_password

    @staticmethod
    def verify_password(hash_password: str, password: str) -> bool:
        return check_password_hash(hash_password, password)

    def __str__(self) -> str:
        return f"{self.id}-{self.first_name}-{self.last_name}"
