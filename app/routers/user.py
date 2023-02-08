
from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime


from .. import schemas, models, utils, database

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.get("/", response_model=List[schemas.User])
async def get_users(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users


@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.CreateUser, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(
        models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user.password = utils.hash(user.password)
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/{id}", response_model=schemas.User)
async def get_user_by_id(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    print(user.orders)
    return user
