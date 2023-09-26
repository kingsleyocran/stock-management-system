from typing import Union

from sqlalchemy import orm

from models.users import Users
from schemas.users import RegisterUserIn
from utils import sql

error_msg = "Please verify your email first"


class UserCheckers:
    def __init__(self, db: orm.Session) -> None:
        self._db = db

    def get_user_by(self, id_or_email: Union[int, str]) -> Users:
        if isinstance(id_or_email, int):
            user_found = self._db.query(Users).filter(Users.id == id_or_email).first()

        elif isinstance(id_or_email, str):
            user_found = (
                self._db.query(Users).filter(Users.email == id_or_email).first()
            )

        else:
            raise ValueError("id_or_email must be an integer or string")

        if not user_found:
            raise ValueError("User not found")

        return user_found

    def check_if_user_exists(self, id: int) -> bool:
        user_found = self.get_user_by(id)
        if user_found:
            return True
        return False

    def check_if_email_exists(self, email: str) -> bool:
        user_found = self.get_user_by(email)
        if user_found:
            return True
        return False

    def is_email_verified(self, id: int) -> bool:
        user_found = self.get_user_by(id)
        return user_found.is_email_verified

    def is_admin(self, id: int) -> bool:
        user_found = self.get_user_by(id)
        return user_found.is_admin

    def is_sales_rep(self, id: int) -> bool:
        user_found = self.get_user_by(id)
        return user_found.role.value == "sales_rep"

    def is_customer(self, id: int) -> bool:
        user_found = self.get_user_by(id)
        return user_found.role.value == "customer"


class UserController:
    def __init__(self, db: orm.Session) -> None:
        self._db = db
        self._checker = UserCheckers(db)

    def register_user(self, user: RegisterUserIn) -> Users:
        hash_password = Users.set_password(user.password)
        new_user = Users(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            hash_password=hash_password,
            gender=user.gender.value,
            role=user.role.value,
        )
        sql.add_item_to_db(self._db, new_user)
        return {
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "email": new_user.email,
            "gender": new_user.gender.value,
            "role": new_user.role.value,
        }

    def register_admin(self, admin_user_id: int, id: int) -> Users:
        user_found = self._checker.get_user_by(id)

        if not self._checker.is_email_verified(id):
            raise ValueError("User has not verified email")

        if not self._checker.is_admin(admin_user_id):
            raise ValueError("You are not authorized to register an Administrator")

        if not self._checker.is_sales_rep(id):
            raise ValueError(
                "Can't register normal customers as Administrators. They must be Sale Reps!"
            )

        user_found.is_admin = True
        sql.add_item_to_db(self._db, user_found)
        return user_found

    def verify_email(self, email: str) -> int:
        user_found = self._checker.get_user_by(email)
        user_found.is_email_verified = True
        sql.add_item_to_db(self._db, user_found)
        return user_found.id

    def verify_password(self, id: int, password: str) -> bool:
        user_found = self._checker.get_user_by(id)
        if not self._checker.is_email_verified(id):
            raise ValueError(error_msg)

        return user_found.verify_password(user_found.hash_password, password)

    def reset_password(self, id: int, new_password: str) -> bool:
        user_found = self._checker.get_user_by(id)
        if not self._checker.is_email_verified(id):
            raise ValueError(error_msg)

        user_found.password = Users.set_password(new_password)
        sql.add_item_to_db(self._db, user_found)
        return True

    def reset_email(self, id: int, email: str):
        user_found = self._checker.get_user_by(id)

        if not self._checker.is_email_verified(id):
            raise ValueError(error_msg)

        user_found.email = email
        sql.add_item_to_db(self._db, user_found)
        return True

    def get_user(self, id_or_email: Union[int, str]) -> Users:
        if not self._checker.is_email_verified(id_or_email):
            raise ValueError(error_msg)

        return self._checker.get_user_by(id_or_email)
