

from pydantic import BaseModel


class CustomerMeta(BaseModel):
    customer_id: int

    class Info():
        table = 'customers'
        pk = ['customer_id']


class Customer(CustomerMeta):
    first_name: str
    last_name: str
    address: str
    city: str
    state: str
    zip_code: str
    email: str
    phone: str

