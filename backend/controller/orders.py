from sqlalchemy import orm

from controller.products import ProductCheckers
from controller.users import UserCheckers, UserController
from models.order import Orders
from models.product import Products
from schemas import orders
from utils import sql


class OrderController:
    def __init__(self, db: orm.Session):
        self._db = db
        self._user_checker = UserCheckers(db)
        self._product_checker = ProductCheckers(db)
        self._user_controller = UserController(db)

    def create_order(
        self, user_id: int, product: orders.OrderBuyIn, total_amount
    ) -> Orders:
        new_order = Orders(
            user_id=user_id,
            product_id=product.product_id,
            quantity=product.quantity,
            total_amount=total_amount,
        )
        sql.add_item_to_db(self._db, new_order)
        return new_order

    def get_order(self, user_id, order_id: int):
        order = self._db.query(Orders).filter(Orders.id == order_id).first()
        if order.user_id != user_id or not self._user_checker.is_admin(user_id):
            raise ValueError("You can't access this order")

        if not order:
            raise ValueError(f"Order #{order_id} not found")
        return order

    def there_are_enough_products(self, original: Products, quantity) -> bool:
        return original.quantity >= quantity

    def toggle_product_status_to_unavailable(self, original: Products) -> bool:
        """
        Note: Toggle Product Status to Unavailable when the
        quantity of product is finished or 0
        """
        if original.quantity == 0:
            original.status = "unavailable"
            return sql.add_item_to_db(self._db, original)

    def subtract_quantity_from_original_product(
        self, original: Products, new_quantity
    ) -> None:
        """
        Note: Substract quantity of product from the existing one
        if the result of the operation leads to the quantity
        being finished  or quantity = 0, toggle the product
        to unavaible status
        """
        original.quantity = original.quantity - new_quantity
        sql.add_item_to_db(self._db, original)
        self.toggle_product_status_to_unavailable(original)

    def compute_total_amount(self, quantity: int, price: float):
        return quantity * price

    def buy_products(
        self, user_id: int, products: list[orders.OrderBuyIn]
    ) -> list[orders.OrderBuyOut]:
        constraint = (
            self._user_checker.is_customer(user_id)
            or self._user_checker.is_sales_rep(user_id)
        ) and self._user_checker.is_email_verified(user_id)
        if not constraint:
            raise ValueError("Can't Order any product, please register first with us")

        result = []

        # check if there is enough products for each order
        for product in products:
            product_id = product.product_id
            product_found = self._product_checker.get_product(product_id)
            user_found = self._user_controller.get_user(user_id)

            if not self.there_are_enough_products(product_found, product.quantity):
                raise ValueError(
                    f"We don't have enough {product_found.name} available, Just {product_found.quantity} left!"
                )

        # process all orders
        for product in products:
            self.subtract_quantity_from_original_product(
                product_found, product.quantity)
            total_amount = self.compute_total_amount(
                product.quantity, product_found.price)

            new_order = self.create_order(user_id, product, total_amount)

            data: orders.OrderBuyOut = {
                "name": f"{user_found.first_name} {user_found.last_name}",
                "product_name": product_found.name,
                "quantity": new_order.quantity,
                "price": product_found.price,
                "status": new_order.status.value,
                "total_amount": total_amount,
            }
            result.append(data)
        return result

    def format_order(self, order: Orders):
        product = self._product_checker.get_product(order.product_id)
        return {
            "product_name": product.name,
            "quantity": order.quantity,
            "product_price": product.price,
            "status": order.status.value,
            "total_amount": order.total_amount,
        }

    def get_orders_for_a_user(self, user_id: int):
        user_found = self._user_controller.get_user(user_id)

        if not user_found and not self._user_checker.is_admin(user_id):
            raise ValueError("You can't access this order")

        return list(map(self.format_order, user_found.orders))
