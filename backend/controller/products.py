from typing import Any, Union

from sqlalchemy import orm, or_
from sqlalchemy_imageattach.context import store_context

from config import setting
from controller.users import UserCheckers, UserController
from models.product import Products
from schemas import products
from utils import sql
from schemas import products as productsSchema

settings = setting.FileStorage()


class ProductCheckers:
    def __init__(self, db: orm.Session):
        self._db = db
        self._checker = UserCheckers(db)

    def get_product(self, id: int) -> Products:
        product = self._db.query(Products).filter(Products.id == id).first()
        if not product:
            raise ValueError("Product not found")
        return product

    def product_belongs_to_owner(self, user_id: int, product_id: int) -> bool:
        product = self.get_product(product_id)

        if not product:
            return False
        return product.owner_id == user_id

    def can_modify_product(self, user_id: int, product_id: int) -> int:
        return self._checker.is_admin(user_id) and self.product_belongs_to_owner(
            user_id, product_id
        )


class ProductController:
    def __init__(self, db: orm.Session):
        self._db = db
        self._checker = UserCheckers(db)
        self._product_checker = ProductCheckers(db)
        self._user_controller = UserController(db)

    def get_product_with_name(self, name: str) -> list[Products]:
        product_list = []
        search_name = f"{name}%"
        data = self._db.query(Products).filter(or_(Products.name.ilike(
            search_name), Products.category.ilike(search_name))).all()
        for product in data:
            fs_store = settings.get_product_store()
            with store_context(fs_store):
                try:
                    product_pic = product.image.locate()
                except IOError:
                    product_pic = ""
                product_list.append(
                    {
                        "id": product.id,
                        "name": product.name,
                        "price": product.price,
                        "quantity": product.quantity,
                        "description": product.description,
                        "category": product.category,
                        "status": product.status,
                        "image": product_pic,
                    }
                )
        return product_list

    def get_product(self, product_id: int) -> Products:
        return self._product_checker.get_product(product_id)

    def add_product(
        self, user_id: int, product: products.ProductCreate
    ) -> Union[Products, None]:
        user = self._user_controller.get_user(user_id)
        if not self._checker.is_admin(user_id):
            raise ValueError("User is not authorized to add product")

        new_product = Products(
            name=product.name,
            price=product.price,
            quantity=product.quantity,
            category=product.category,
            description=product.description,
            owner_id=user.id,
        )
        sql.add_item_to_db(self._db, new_product)
        return new_product

    def add_image_to_product(
        self, user_id: int, product_id: int, product_image: bytes
    ) -> bool:
        if not self._product_checker.can_modify_product(user_id, product_id):
            raise ValueError("User is not authorized to modify product")

        product = self._product_checker.get_product(product_id)
        fs_store = settings.get_product_store()
        with store_context(fs_store):
            product.image.from_blob(product_image)
            return sql.add_item_to_db(self._db, product)

    def modify_product(
        self, user_id: int, product_id: int, data: products.ProductUpdateIn
    ) -> bool:
        if not self._product_checker.can_modify_product(user_id, product_id):
            raise ValueError("User is not authorized to modify Product")
        product = self._product_checker.get_product(product_id)
        product.name = data.name
        product.price = data.price
        product.quantity = data.quantity
        product.description = data.description
        product.category = data.category
        return sql.add_item_to_db(self._db, product)

    def delete_product(self, user_id: int, product_id: int) -> bool:
        if not self._product_checker.can_modify_product(user_id, product_id):
            raise ValueError("User is not authorized to delete product")
        product = self._product_checker.get_product(product_id)
        fs_store = settings.get_product_store()
        with store_context(fs_store):
            return sql.delete_item_from_db(self._db, product)

    def get_all_products(self) -> list[productsSchema.ProductsListOut]:
        product_list: Any = []
        products = self._db.query(Products).all()
        for product in products:
            fs_store = settings.get_product_store()
            with store_context(fs_store):
                try:
                    product_pic = product.image.locate()
                except IOError:
                    product_pic = ""
                product_list.append(
                    {
                        "id": product.id,
                        "name": product.name,
                        "price": product.price,
                        "quantity": product.quantity,
                        "description": product.description,
                        "category": product.category,
                        "status": product.status,
                        "image": product_pic,
                    }
                )
        return product_list
