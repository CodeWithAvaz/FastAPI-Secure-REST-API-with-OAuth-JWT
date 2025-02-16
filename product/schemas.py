from pydantic import BaseModel


class Product(BaseModel):
    name: str
    description: str 
    price: int


class DisplayProduct(BaseModel):
    name: str
    description: str 

    class Config:
        orm_mode = True



class Seller(BaseModel):
    username: str
    email: str
    password: str