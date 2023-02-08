from sqlalchemy import Column, Integer, String, Float, DateTime, text, ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base


class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    password = Column(String(1024), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False)
    password = Column(String(1024), nullable=False)
    address = Column(String(1024), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    orders = relationship('Order', back_populates='user')
    payments = relationship('Payment', back_populates='user')
    reviews = relationship('Review', back_populates='user')


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1024), nullable=False)
    price = Column(Float, nullable=False)
    image_url = Column(String(1024), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

    reviews = relationship('Review', back_populates='product')


class Review(Base):
    __tablename__ = 'reviews'

    # id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey(
        'products.id', ondelete='CASCADE'), primary_key=True)
    user_id = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), primary_key=True)
    comment = Column(String(1024), nullable=False)
    rating = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

    product = relationship('Product', back_populates='reviews')
    user = relationship('User', back_populates='reviews')


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    order_date = Column(TIMESTAMP(timezone=True), nullable=False)
    total_price = Column(Float, nullable=False)
    shipping_address = Column(String(1024), nullable=False)
    status = Column(String(32), default='pending', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    user = relationship('User', back_populates='orders')
    items = relationship('OrderItem', back_populates='order')
    # payment = relationship('Payment')


class OrderItem(Base):
    __tablename__ = 'order_items'

    order_id = Column(Integer, ForeignKey(
        'orders.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    product_id = Column(Integer, ForeignKey(
        'products.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    order = relationship('Order', back_populates='items')
    product = relationship('Product')


class Payment(Base):
    __tablename__ = 'payments'

    user_id = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    order_id = Column(Integer, ForeignKey(
        'orders.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    payment_date = Column(TIMESTAMP(timezone=True), nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    user = relationship('User', back_populates='payments')
    # order = relationship('Order', back_populates='payment')
