from fastapi import APIRouter, Depends, File, responses
from sqlalchemy.orm import Session

from controller.accounts import AccountController
from controller.auth import AuthController, bearerschema
from schemas import accounts
from utils import session

router = APIRouter(prefix="/accounts")


@router.post("/login")
async def login_user(
    user: accounts.LoginIn,
    authorize: AuthController = Depends(),
    db: Session = Depends(session.create),
):
    account_operation = AccountController(db)
    user_auth = account_operation.login_user(user)
    access_token = authorize.create_access_token(subject=user_auth.id)
    refresh_token = authorize.create_refresh_token(subject=user_auth.id)
    return responses.JSONResponse(
        {"access_token": access_token, "refresh_token": refresh_token}
    )


@router.post("/logout")
async def logout_user(
    _: str = Depends(bearerschema),
    authorize: AuthController = Depends(),
    db: Session = Depends(session.create),
):
    account_operation = AccountController(db)
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()

    if account_operation.logout_user(user_id):
        return responses.JSONResponse({"message": "logged out successfully"})


@router.post("/refresh")
async def get_new_access_token(
    _: str = Depends(bearerschema),
    authorize: AuthController = Depends(),
):
    """
    This API route is use to generate a
    new Access token
    """
    authorize.jwt_refresh_token_required()
    user_id = authorize.get_jwt_subject()
    access_token = authorize.create_access_token(user_id)
    refresh_token = authorize.create_refresh_token(user_id)

    return responses.JSONResponse(
        content={"access_token": access_token, "refresh_token": refresh_token},
        status_code=200,
    )


@router.post("/upload/profile/pic")
async def upload_profile_pic(
    authorize: AuthController = Depends(),
    _: str = Depends(bearerschema),
    profile_pic: bytes = File(...),
    db: Session = Depends(session.create),
):
    authorize.jwt_required()
    account_operation = AccountController(db)
    user_id = authorize.get_jwt_subject()
    if account_operation.upload_profile_pic(user_id, profile_pic):
        return responses.JSONResponse({"message": "profile pic uploaded successfully"})


@router.get("/details", response_model=accounts.DetailsOut)
async def get_account_details(
    authorize: AuthController = Depends(),
    _: str = Depends(bearerschema),
    db: Session = Depends(session.create),
):
    authorize.jwt_required()
    account_operation = AccountController(db)
    user_id = authorize.get_jwt_subject()
    user_details = account_operation.get_account_details(user_id)
    return user_details
