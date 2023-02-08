from fastapi import APIRouter, FastAPI, Response, status, HTTPException, Depends
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from .. import schemas, models, database, oauth2

router = APIRouter(
    prefix="/products",
    tags=['Products']
)


@ router.get('/', response_model=List[schemas.Product])
async def get_products(db: Session = Depends(database.get_db), skip: int = 0, limit: int = 10, search: Optional[str] = ""):
    prods = db.query(models.Product).filter(or_(models.Product.name.ilike(
        f"%{search}%"), models.Product.description.ilike(f"%{search}%"))).offset(skip).limit(limit).all()

    # results = db.query(models.Product.id.label('id'), models.Product.name.label('name'), models.Product.description.label('description'), models.Product.image_url.label('image_url'), models.Product.price.label('price'), models.Product.created_at.label('created_at'), models.Product.updated_at.label('updated_at'), func.avg(models.Review.rating).label("rate")).join(
    #     models.Review, models.Review.product_id == models.Product.id, isouter=True).group_by(models.Product.id).all()
    # print(results)
    return prods


@ router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Product)
async def create_product(prod: schemas.CreateProduct, db: Session = Depends(database.get_db), current_admin: schemas.Admin = Depends(oauth2.get_current_admin)):
    new_prod = models.Product(**prod.dict())
    db.add(new_prod)
    db.commit()
    db.refresh(new_prod)
    # print('admin id:', admin.id)
    return new_prod


@ router.get('/{id}', response_model=schemas.Product)
async def get_product_by_id(id: int, db: Session = Depends(database.get_db),):
    prod = db.query(models.Product).filter(models.Product.id == id).first()
    if not prod:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Product with id: {id} was not found!')
    return prod


@ router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: int, db: Session = Depends(database.get_db), current_admin: schemas.Admin = Depends(oauth2.get_current_admin)):
    prod_query = db.query(models.Product).filter(models.Product.id == id)
    if not prod_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Product with id: {id} was not found!')
    prod_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.Product)
async def update_product(id: int, update_data: schemas.UpdateProduct, db: Session = Depends(database.get_db), current_admin: schemas.Admin = Depends(oauth2.get_current_admin)):
    prod = db.query(models.Product).filter_by(id=id).first()
    if not prod:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Product with id: {id} was not found!')

    for key, value in update_data.dict().items():
        if value is not None:
            setattr(prod, key, value)
    prod.updated_at = datetime.now()
    db.commit()
    db.refresh(prod)

    return prod


@router.post("/{product_id}/reviews", response_model=schemas.Review)
async def create_review(
    product_id: int, review: schemas.ReviewCreate, db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user)
):
    db_product = db.query(models.Product).get(product_id)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Product not found")
    print(product_id, current_user.id)
    db_review = db.query(models.Review).filter(and_(
        models.Review.product_id == product_id, models.Review.user_id == current_user.id)).first()
    # print(db_review.dict())
    if db_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="This user has made a review before")
    review = models.Review(
        product_id=product_id,
        user_id=current_user.id,
        **review.dict()
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@router.put("/{product_id}/reviews", response_model=schemas.Review)
async def update_review(
    product_id: int,  review: schemas.UpdateReview, db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user)
):
    db_review = db.query(models.Review).filter(and_(
        models.Review.product_id == product_id, models.Review.user_id == current_user.id)).first()
    if not db_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Review not found")

    for key, value in review.dict().items():
        if value is not None:
            setattr(db_review, key, value)

    db.commit()
    db.refresh(db_review)
    return db_review


@ router.delete('/{product_id}/reviews', status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(product_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    review_query = db.query(models.Review).filter(and_(
        models.Review.user_id == current_user.id, models.Review.product_id == product_id))
    if not review_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Review was not found')
    review_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
