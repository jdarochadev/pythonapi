from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str

    @field_validator('price')
    def validate_price(cls, v):
        if v < 0:
            raise ValueError('Price must be greater than or equal to 0')
        return v

    @field_validator('name')
    def validate_name(cls, v):
        if len(v) > 100:
            raise ValueError('Name must not exceed 100 characters')
        return v

    @field_validator('category')
    def validate_category(cls, v):
        if len(v) > 50:
            raise ValueError('Category must not exceed 50 characters')
        return v

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None

    @field_validator('price')
    def validate_price(cls, v):
        if v is not None and v < 0:
            raise ValueError('Price must be greater than or equal to 0')
        return v

    @field_validator('name')
    def validate_name(cls, v):
        if v is not None and len(v) > 100:
            raise ValueError('Name must not exceed 100 characters')
        return v

    @field_validator('category')
    def validate_category(cls, v):
        if v is not None and len(v) > 50:
            raise ValueError('Category must not exceed 50 characters')
        return v

class ProductPatch(ProductUpdate):
    pass

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    category: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
