from fastapi import APIRouter, Depends, File, responses, Body
from sqlalchemy.orm import Session
from fastapi_pagination.links import Page
from fastapi_pagination import paginate


from controller.auth import AuthController, bearerschema
from controller.products import ProductController
from schemas import products
from utils import session
from typing import Union

router = APIRouter(prefix="/products")


@router.get("/all", response_model=Page[products.ProductsListOut])
async def get_all_products(db: Session = Depends(session.create)) -> Page[products.ProductsListOut]:
    product_operation = ProductController(db)
    data = product_operation.get_all_products()
    return paginate(data)


@router.get("/{product_id}", response_model=products.ProductSingleOut)
async def get_details_of_a_product(product_id: Union[int, str], db: Session = Depends(session.create)):
    product_operation = ProductController(db)
    print("working with this")
    return product_operation.get_product(product_id)


@router.get("/name/{name}", response_model=list[products.ProductsListOut])
async def retrieve_all_products_with_name(name: str, db: Session = Depends(session.create)):
    product_operation = ProductController(db)
    return product_operation.get_product_with_name(name)


@router.post("/add", response_model=products.ProductCreateOut)
async def add_product(
    product: products.ProductCreate,
    _: str = Depends(bearerschema),
    authorize: AuthController = Depends(),
    db: Session = Depends(session.create),
):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    product_operation = ProductController(db)
    return product_operation.add_product(user_id, product)


@router.post("/upload/image/{product_id}")
async def upload_product_image(
    product_id: int,
    image: bytes = File(...),
    _: str = Depends(bearerschema),
    authorize: AuthController = Depends(),
    db: Session = Depends(session.create),
):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    product_operation = ProductController(db)
    if product_operation.add_image_to_product(user_id, product_id, image):
        return responses.JSONResponse({"message": "Image uploaded successfully"}, 201)
    return responses.JSONResponse({"message": "Image upload failed"}, 203)


@router.put("/update/{product_id}")
async def update_product(
    product_id: int,
    data: products.ProductUpdateIn,
    _: str = Depends(bearerschema),
    authorize: AuthController = Depends(),
    db: Session = Depends(session.create),
):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    product_operation = ProductController(db)
    if product_operation.modify_product(user_id, product_id, data):
        return responses.JSONResponse({"message": "Modified Product successfully"})


@router.delete("/remove/{product_id}")
async def delete_product(
    product_id: int,
    _: str = Depends(bearerschema),
    authorize: AuthController = Depends(),
    db: Session = Depends(session.create),
):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    product_operation = ProductController(db)
    if product_operation.delete_product(user_id, product_id):
        return responses.JSONResponse({"message": "Product deleted"}, 204)
