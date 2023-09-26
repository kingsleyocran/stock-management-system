from pydantic import BaseModel, EmailStr


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class LoginOut(BaseModel):
    access_token: str
    refresh_token: str


class DetailsOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    profile_pic: str
    is_admin: bool
    is_sales_rep: bool
