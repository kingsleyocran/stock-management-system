from pydantic import BaseModel, EmailStr

from schemas.enums import Gender, Role


class RegisterUserIn(BaseModel):
    """Register User Schema"""

    first_name: str
    last_name: str
    password: str
    email: EmailStr
    gender: Gender
    role: Role

    class Config:
        orm_mode = True


class RegisterUserOut(BaseModel):
    """Register User Schema"""

    message: str
    data: dict[str, str]

    class Config:
        orm_mode = True


class RegisterAdminIn(BaseModel):
    """Register Admin Schema"""

    user_id: int

    class Config:
        orm_mode = True


class RegisterAdminOut(BaseModel):
    """Register Admin Schema"""

    message: str


class EmailVerifyIn(BaseModel):
    """Email Verify Schema"""

    email: str


class ResetEmailIn(BaseModel):
    """Reset Email Schema"""

    email: str


class ResetPasswordIn(BaseModel):
    """Reset Password Schema"""

    password: str
