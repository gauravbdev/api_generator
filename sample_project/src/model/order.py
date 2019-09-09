

from pydantic import BaseModel


class OrderMeta(BaseModel):
    order_id: int

    class Info():
        table = 'orders'
        pk = ['order_id']


class Order(OrderMeta):
    customer_id: int
    created_datetime: int
    is_paid: str

