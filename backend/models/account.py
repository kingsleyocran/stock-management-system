from datetime import datetime

import sqlalchemy as sq
from sqlalchemy.orm import relationship
from sqlalchemy_imageattach.entity import Image, image_attachment

from core import setup


class Accounts(setup.Base):
    __tablename__ = "accounts"
    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(
        sq.Integer, sq.ForeignKey("users.id"), unique=True, nullable=False
    )
    picture = image_attachment("UserPicture")
    is_logged_in = sq.Column(sq.Boolean, default=False)
    created_at = sq.Column(sq.DateTime, default=datetime.utcnow())
    updated_at = sq.Column(
        sq.DateTime, default=datetime.utcnow(), onupdate=datetime.now()
    )

    def __str__(self) -> str:
        return f"user-{self.user_id}"

    def __repr__(self):
        return f"Account(id={self.id})"


class UserPicture(setup.Base, Image):
    """User picture model."""

    user_id = sq.Column(sq.Integer, sq.ForeignKey("accounts.id"), primary_key=True)
    user = relationship("Accounts", overlaps="picture", lazy="select")
    __tablename__ = "user_picture"
