from fastapi import FastAPI, status, Response, HTTPException
from sqlalchemy.sql.functions import mode
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext

from . import schemas
from . import models
from .database import engine, SessionLocal
app = FastAPI()

models.Base.metadata.create_all(engine)

pwd_content = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

@app.get("/products", response_model=List[schemas.DisplayProduct])
def products(db: Session = Depends(get_db)):
    all_products = db.query(models.Product).all()
    return all_products

@app.get("/product/{id}/", response_model=schemas.DisplayProduct)
def product(id, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Not Found")
    return product
    

@app.delete("/product/{id}")
def product_delete(id, db: Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return f"Product Successfully deleted"


@app.put("/product/{id}")
def product_delete(id, request: schemas.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        pass
    product.update(request.dict())
    db.commit()
    return "Product successfully Updated"


@app.post("/product", status_code=201)
def add(request: schemas.Product, db: Session = Depends(get_db)):
    new_product = models.Product(
        name=request.name,
        description=request.description,
        price=request.price
        )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

#----------

@app.post("/seller")
def create_seller(request: schemas.Seller, db: Session = Depends(get_db)):
    hashedpassword = pwd_content.hash(request.password)
    new_seller = models.Seller(
        username=request.username,
        email=request.email,
        password=hashedpassword
    )
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller