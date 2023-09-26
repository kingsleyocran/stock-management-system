from pydantic import BaseModel, validator

from .enums import OrderStatus


class OrderBuyIn(BaseModel):
    product_id: int
    quantity: int

    @validator("quantity")
    def check_quantity(cls, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be more than 0")
        return quantity

    class Config:
        orm_mode = True


class OrderBuyOut(BaseModel):
    name: str
    product_name: str
    quantity: str
    price: float
    total_amount: float
    status: OrderStatus


class OrderUserOut(BaseModel):
    product_name: str
    quantity: int
    product_price: float
    total_amount: float
    status: OrderStatus

    class Config:
        orm_mode = True


class OrderSingleOut(BaseModel):
    product_id: int
    user_id: int
    quantity: int
    total_amount: float
    status: OrderStatus

    class Config:
        orm_mode = True
