import uuid
from datetime import datetime

import sqlalchemy as sq
from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy_imageattach.entity import Image, image_attachment

from core import setup
from schemas.enums import ProductStatus


class Products(setup.Base):
    __tablename__ = "products"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String, nullable=False, unique=True)
    price = sq.Column(sq.Float, nullable=False)
    description = sq.Column(sq.String, nullable=False)
    # tag = sq.Column(UUID(as_uuid=True), name="uuid", unique=True, default=uuid.uuid4())
    image = image_attachment("ProductPicture")
    category = sq.Column(sq.String, nullable=False)
    quantity = sq.Column(sq.Integer, nullable=False)
    status = sq.Column(Enum(ProductStatus), default="available")
    owner_id = sq.Column(sq.Integer, sq.ForeignKey("users.id"), nullable=False)
    orders = relationship("Orders", back_populates="products")
    created_at = sq.Column(sq.DateTime, default=datetime.now())
    updated_at = sq.Column(sq.DateTime, default=datetime.now(), onupdate=datetime.now())


class ProductPicture(setup.Base, Image):
    """Product picture model."""

    product_id = sq.Column(sq.Integer, sq.ForeignKey("products.id"), primary_key=True)
    product = relationship("Products", overlaps="image", back_populates="image")
    __tablename__ = "product_picture"
    __mapper_args__ = {"polymorphic_identity": "product_picture"}
