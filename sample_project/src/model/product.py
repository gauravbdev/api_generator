

from pydantic import BaseModel


class ProductMeta(BaseModel):
    product_id: int

    class Info():
        table = 'products'
        pk = ['product_id']


class Product(ProductMeta):
    name: str
    category: str
    price: float
    available_qty: int
    description: str

