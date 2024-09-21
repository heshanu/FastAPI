from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    name: str
    price: float
    id:int
    is_sale:bool
    inventory:int

