from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, constr


# Payment #
class CreatePayment(BaseModel):
    payment_date: datetime
    amount: float


class Payment(BaseModel):
    user_id: int
    order_id: int
    payment_date: datetime
    amount: float
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Order #


class CreateOrderItem(BaseModel):
    product_id: int
    quantity: int
    price: float


class OrderItem(BaseModel):
    product_id: int
    order_id: int
    quantity: int
    price: float
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True


class CreateOrder(BaseModel):
    order_date: str
    total_price: float
    shipping_address: str
    status: constr(
        regex='^(arrived|in_delivery|pending|cancelled)$') = "pending"
    order_items: List[CreateOrderItem]
    payment: CreatePayment = None


class Order(BaseModel):
    id: int
    order_date: datetime
    total_price: float
    shipping_address: str
    status: constr(regex='^(arrived|in_delivery|pending|cancelled)$')
    updated_at: datetime
    created_at: datetime

    items: List[OrderItem] = []
    # payment: Optional[Payment]

    class Config:
        orm_mode = True


class UpdateOrder(BaseModel):
    status: constr(regex='^(arrived|in_delivery|pending|cancelled)$')


# Reviews #


class ReviewCreate(BaseModel):
    comment: str
    rating: float


class Review(ReviewCreate):
    product_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UpdateReview(BaseModel):
    comment: Optional[str]
    rating: Optional[float]

# Token #


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class TokenDate(BaseModel):
    id: Optional[str] = None
    role: Optional[str] = None

# Admin #


class AdminBase(BaseModel):
    username: str


class Admin(AdminBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CreateAdmin(AdminBase):
    password: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

# User #


class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    orders: List[Order] = []
    payments: List[Payment] = []
    reviews: List[Review] = []

    class Config:
        orm_mode = True


class CreateUser(UserBase):
    password: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Products #


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    image_url: str


class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    reviews: List[Review] = []

    class Config:
        orm_mode = True


class ProductOut(BaseModel):
    product: Product
    rate: Optional[int]

    class Config:
        orm_mode = True


class CreateProduct(ProductBase):
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class UpdateProduct(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    image_url: Optional[str]
    updated_at: Optional[str]
