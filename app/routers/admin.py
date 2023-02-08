
from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime


from .. import schemas, models, utils, database

router = APIRouter(
    prefix="/admins",
    tags=['Admins']
)


@router.get("/", response_model=List[schemas.Admin])
async def get_admins(db: Session = Depends(database.get_db)):
    admins = db.query(models.Admin).all()
    return admins


@router.post("/", response_model=schemas.Admin)
async def create_admin(admin: schemas.CreateAdmin, db: Session = Depends(database.get_db)):
    db_admin = db.query(models.Admin).filter(
        models.Admin.username == admin.username).first()
    if db_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    admin.password = utils.hash(admin.password)
    db_admin = models.Admin(**admin.dict())
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin


@router.get("/{id}", response_model=schemas.Admin)
async def get_admin_by_id(id: int, db: Session = Depends(database.get_db)):
    admin = db.query(models.Admin).filter(models.Admin.id == id).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
    return admin
