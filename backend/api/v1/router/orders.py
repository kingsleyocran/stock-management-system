from fastapi import APIRouter, Depends, responses, Request
from sqlalchemy.orm import Session

from controller.auth import AuthController, bearerschema
from controller.orders import OrderController
from schemas import orders
from utils import session

router = APIRouter(prefix="/orders")


@router.post("/make", response_model=list[orders.OrderBuyOut])
async def make_an_order(
    order: list[orders.OrderBuyIn],
    _: str = Depends(bearerschema),
    authorize: AuthController = Depends(),
    db: Session = Depends(session.create),
):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    order_operation = OrderController(db)
    made_an_order = order_operation.buy_products(user_id, order)
    return responses.JSONResponse(made_an_order, 201)


@router.get("/{order_id}", response_model=orders.OrderSingleOut)
async def retrieve_an_order(
    order_id,
    _: str = Depends(bearerschema),
    authorize: AuthController = Depends(),
    db: Session = Depends(session.create),
):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    order_operation = OrderController(db)
    return order_operation.get_order(user_id, order_id)


@router.get("/user", response_model=list[orders.OrderUserOut])
async def get_all_orders_from_a_user(
    _: str = Depends(bearerschema),
    authorize: AuthController = Depends(),
    db: Session = Depends(session.create),
):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    order_operation = OrderController(db)
    return order_operation.get_orders_for_a_user(user_id)
