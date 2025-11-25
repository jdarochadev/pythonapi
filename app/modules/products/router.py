from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.core.auth import get_current_user
from app.modules.users.models import User
from app.modules.products.schemas import ProductCreate, ProductUpdate, ProductPatch, ProductResponse
from app.modules.products.repository import (
    get_products,
    get_product_by_id,
    create_product,
    update_product,
    patch_product,
    delete_product
)

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[ProductResponse])
def list_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    products = get_products(db, skip=skip, limit=limit)
    return products

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_new_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = create_product(db, product_data)
    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update_existing_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = update_product(db, product_id, product_data)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product

@router.patch("/{product_id}", response_model=ProductResponse)
def patch_existing_product(
    product_id: int,
    product_data: ProductPatch,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = patch_product(db, product_id, product_data)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = delete_product(db, product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
