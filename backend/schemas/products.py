from typing import Any

from pydantic import BaseModel, root_validator, validator

from .enums import ProductStatus


class ProductCreate(BaseModel):
    name: str
    price: float
    quantity: int
    description: str
    category: str

    @validator("quantity")
    def check_quantity(cls, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be more than 0")
        return quantity

    @validator("price")
    def check_price(cls, price):
        if price <= 0:
            raise ValueError("Price must be more than 0")
        return price

    @root_validator
    def _check_fields(cls, values):
        name = values.get("name")
        values["name"] = name.capitalize()
        return values

    class Config:
        orm_mode = True


class ProductCreateOut(BaseModel):
    id: int
    owner_id: int
    name: str
    price: float
    quantity: int
    description: str
    category: str

    class Config:
        orm_mode = True


class ProductUpdateIn(BaseModel):
    name: str
    price: float
    quantity: int
    description: str
    category: str

    @validator("quantity")
    def check_quantity(cls, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be more than 0")
        return quantity

    @validator("price")
    def check_price(cls, price):
        if price <= 0:
            raise ValueError("Price must be more than 0")
        return price

    @root_validator
    def _check_fields(cls, values):
        name = values.get("name")
        values["name"] = name.capitalize()
        return values

    class Config:
        orm_mode = True


class ProductsListOut(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    description: str
    category: str
    status: ProductStatus
    image: Any

    class Config:
        orm_mode = True


class ProductSingleOut(BaseModel):
    id: int
    name: str
    price: float
    description: str
    category: str
    quantity: int
    status: ProductStatus

    class Config:
        orm_mode = True
