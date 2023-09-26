from fastapi import APIRouter, BackgroundTasks, Depends, Request, responses, templating
from sqlalchemy.orm import Session

from config import setting
from controller.accounts import AccountController
from controller.auth import AuthController, bearerschema
from controller.users import UserController
from plugins import email
from schemas import users
from utils import session

settings = setting.AppSettings()

router = APIRouter(prefix="/users")
templates = templating.Jinja2Templates(directory="templates")


@router.post(
    "/register",
    response_model=users.RegisterUserOut,
)
async def register_user(
    user: users.RegisterUserIn,
    background_task: BackgroundTasks,
    authorize: AuthController = Depends(),
    db: Session = Depends(session.create),
):
    user_operation = UserController(db)
    data = user_operation.register_user(user)
    access_token = authorize.create_access_token(user.email)
    email_controller = email.Email()
    email_controller.send_email_background(
        background_task=background_task,
        subject="Verify Your Account",
        to=data.get("email"),
        content={
            "title": "Verify Your Account",
            "content": "Please verify your account by clicking the button below. Link expires in 3 mins",
            "name": f"Hi {data.get('first_name').capitalize()}!",
            "endpoint": f"{settings.SERVER_NAME}{settings.API_PREFIX}/users/verify/email?token={access_token}",
        },
    )
    return responses.JSONResponse(
        {
            "message": "User created successfully",
            "data": data,
        }
    )


@router.post(
    "/register/admin",
)
async def register_admin(
    user: users.RegisterAdminIn,
    authorize: AuthController = Depends(),
    _: str = Depends(bearerschema),
    db: Session = Depends(session.create),
):
    authorize.jwt_required()
    admin_user_id = authorize.get_jwt_subject()
    user_operation = UserController(db)
    if user_operation.register_admin(admin_user_id, user.user_id):
        return responses.JSONResponse({"message": "Admin added successfully"})


@router.get("/verify/email")
async def verify_email(
    token: str,
    request: Request,
    authorize: AuthController = Depends(),
    db: Session = Depends(session.create),
):
    user_email = authorize.get_raw_jwt(token)["sub"]
    user_operation = UserController(db)
    account_operation = AccountController(db)
    user_id = user_operation.verify_email(user_email)
    _ = account_operation.create_account(user_id)
    return templates.TemplateResponse(
        "activated.html",
        {
            "request": request,
            "frontend_url": settings.FRONTEND_URL,
            "app_name": settings.APP_TITLE.capitalize(),
        },
    )


@router.put("/reset/email")
async def reset_email(
    user: users.ResetEmailIn,
    authorize: AuthController = Depends(),
    _: str = Depends(bearerschema),
    db: Session = Depends(session.create),
):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    user_operation = UserController(db)
    user_found = user_operation.get_user(user_id)
    if user_operation.reset_email(user_found.id, user.email):
        return responses.JSONResponse({"message": "Email reset successfully"})
    return responses.JSONResponse({"error": "Failed to reset email"}, 400)


@router.put("/reset/password")
async def reset_password(
    user: users.ResetPasswordIn,
    authorize: AuthController = Depends(),
    _: str = Depends(bearerschema),
    db: Session = Depends(session.create),
):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    user_operation = UserController(db)
    user_found = user_operation.get_user(user_id)
    if user_operation.reset_password(user_found.id, user.password):
        return responses.JSONResponse({"message": "Password reset successfully"})
    return responses.JSONResponse({"error": "Failed to reset password"})
