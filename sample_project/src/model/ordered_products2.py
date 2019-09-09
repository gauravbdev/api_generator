

from pydantic import BaseModel


class Ordered_products2Meta(BaseModel):
    order_id: int
    product_id: int

    class Info():
        table = 'ordered_products2'
        pk = ['order_id', 'product_id']


class Ordered_products2(Ordered_products2Meta):
    qty: int

