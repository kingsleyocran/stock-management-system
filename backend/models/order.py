from datetime import datetime

import sqlalchemy as sq
from sqlalchemy.orm import relationship

from core import setup
from schemas.enums import OrderStatus


class Orders(setup.Base):
    __tablename__ = "orders"
    id = sq.Column(sq.Integer, primary_key=True)
    occured_at = sq.Column(sq.DateTime, default=datetime.now())
    product_id = sq.Column(sq.Integer, sq.ForeignKey("products.id"))
    user_id = sq.Column(sq.Integer, sq.ForeignKey("users.id"))
    quantity = sq.Column(sq.Integer, nullable=False)
    status = sq.Column(sq.Enum(OrderStatus), nullable=False, default="on_the_way")
    total_amount = sq.Column(sq.Float, nullable=False)
    users = relationship("Users", back_populates="orders")
    products = relationship("Products", back_populates="orders")
