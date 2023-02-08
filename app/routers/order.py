from fastapi import APIRouter, FastAPI, Response, status, HTTPException, Depends
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from .. import schemas, models, database, oauth2

router = APIRouter(
    prefix="/orders",
    tags=['Orders']
)


@ router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Order)
async def create_order(order: schemas.CreateOrder, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    try:
        new_order = models.Order(user_id=current_user.id, order_date=order.order_date,
                                 total_price=order.total_price, shipping_address=order.shipping_address, status=order.status)
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        items_to_commit = []
        for item in order.order_items:
            order_item: schemas.CreateOrderItem = item
            db_product = db.query(models.Product).get(order_item.product_id)
            if not db_product:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Product not found")
            order_item = models.OrderItem(
                order_id=new_order.id,
                **order_item.dict()
            )
            items_to_commit.append(order_item)
        db.add_all(items_to_commit)
        db.commit()

        if order.payment:
            payment = models.Payment(
                order_id=new_order.id,
                user_id=current_user.id,
                **order.payment.dict()
            )
            db.add(payment)
            db.commit()
            db.refresh(payment)
    except:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred")
    return new_order


@router.get('/{id}', response_model=schemas.Order)
async def get_order_by_id(id: int, db: Session = Depends(database.get_db)):
    order = db.query(models.Order).filter(models.Order.id == id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Order with id: {id} was not found')
    return order


@router.put('/{id}', response_model=schemas.Order)
async def update_order(id: int, update_data: schemas.UpdateOrder, db: Session = Depends(database.get_db), current_admin: schemas.Admin = Depends(oauth2.get_current_admin)):
    order = db.query(models.Order).filter_by(id=id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Order with id: {id} was not found')

    for key, value in update_data.dict().items():
        if value is not None:
            setattr(order, key, value)
    order.updated_at = datetime.now()
    db.commit()
    db.refresh(order)

    return order


@router.get('/payments/{order_id}', response_model=schemas.Payment)
def get_user_payment_by_order_id(order_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    db_payment = db.query(models.Payment).filter(and_(
        models.Payment.user_id == current_user.id, models.Payment.order_id == order_id)).first()
    if not db_payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Payment was not found')
    return db_payment


# @ router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
# async def delete_order(id: int, db: Session = Depends(database.get_db), current_user: schemas.Admin = Depends(oauth2.get_current_admin)):
#     order_query = db.query(models.Order).filter(models.Order.id == id)
#     if not order_query.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#     detail=f'Order with id: {id} was not found')
#     order_query.delete(synchronize_session=False)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @router.post("/{order_id}/orderitems", response_model=schemas.OrderItem)
# async def create_order_item(
#     order_id: int,  order_item: schemas.CreateOrderItem, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)
# ):
#     db_order = db.query(models.Order).get(order_id)
#     if not db_order:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="Order not found")
#     db_product = db.query(models.Product).get(order_item.product_id)
#     if not db_product:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="Product not found")
#     order_item = models.OrderItem(
#         order_id=order_id,
#         **order_item.dict()
#     )
#     db.add(order_item)
#     db.commit()
#     db.refresh(order_item)
#     return order_item
