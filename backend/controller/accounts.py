from sqlalchemy import orm
from sqlalchemy_imageattach.context import store_context

from config import setting
from controller.users import UserController
from models.account import Accounts
from schemas import accounts
from utils import sql

settings = setting.FileStorage()


class AccountController:
    def __init__(self, db: orm.Session):
        self._db = db
        self._user_checker = UserController(db)

    def get_account_by(self, user_id: int) -> Accounts:
        account = self._db.query(Accounts).filter(Accounts.user_id == user_id).first()
        if not account:
            raise ValueError("Account not found")
        return account

    def create_account(self, email: str) -> Accounts:
        user_found = self._user_checker.get_user(email)
        new_account = Accounts(user_id=user_found.id)
        sql.add_item_to_db(self._db, new_account)
        return new_account

    def get_account_details(self, user_id: int) -> accounts.DetailsOut:
        account = self.get_account_by(user_id)
        user = self._user_checker.get_user(user_id)
        fs_store = settings.get_profile_store()

        try:
            with store_context(fs_store):
                profile_pic = account.picture.locate()
        except OSError:
            profile_pic = ""

        data = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "profile_pic": profile_pic,
            "is_admin": user.is_admin,
            "is_sales_rep": self._user_checker._checker.is_sales_rep(user.id)
        }
        return data

    def upload_profile_pic(self, user_id: int, profile_pic: bytes):
        user = self.get_account_by(user_id)
        fs_store = settings.get_profile_store()
        with store_context(fs_store):
            user.picture.from_blob(profile_pic)
            sql.add_item_to_db(self._db, user)
            return True

    def login_user(self, user_details: accounts.LoginIn):
        user = self._user_checker.get_user(user_details.email)
        if not user:
            raise ValueError("User not found")

        if not self._user_checker.verify_password(user.id, user_details.password):
            raise ValueError("Invalid password")

        account = self.get_account_by(user.id)
        account.is_logged_in = True
        sql.add_item_to_db(self._db, account)
        return user

    def logout_user(self, user_id: str):
        user = self._user_checker.get_user(user_id)
        account = self.get_account_by(user.id)
        if not user or not account:
            raise ValueError("User not found")

        account.is_logged_in = False
        sql.add_item_to_db(self._db, account)
        return True
