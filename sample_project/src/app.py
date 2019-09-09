
from fastapi import FastAPI
from util import sql as sq
from util import postgres as pg
import json

from model.customer import *
from model.order import *
from model.product import *

app = FastAPI(docs_url='/')


@app.get('/get_customer/{customer_id}')
async def get_customer(customer_id: int):
    d = {"customer_id": customer_id}
    customer_meta = CustomerMeta(**d)
    return _get(customer_meta)


@app.delete('/delete_customer/{customer_id}')
async def delete_customer(customer_id: int):
    d = {"customer_id": customer_id}
    customer_meta = CustomerMeta(**d)
    return _delete(customer_meta)


@app.post('/add_customer')
async def add_customer(customer: Customer):
    customer.customer_id = None
    return _add(customer)
    
@app.put('/update_customer')
async def update_customer(customer: Customer):
    return _update(customer)


@app.get('/get_order/{order_id}')
async def get_order(order_id: int):
    d = {"order_id": order_id}
    order_meta = OrderMeta(**d)
    return _get(order_meta)


@app.delete('/delete_order/{order_id}')
async def delete_order(order_id: int):
    d = {"order_id": order_id}
    order_meta = OrderMeta(**d)
    return _delete(order_meta)


@app.post('/add_order')
async def add_order(order: Order):
    order.order_id = None
    return _add(order)
    
@app.put('/update_order')
async def update_order(order: Order):
    return _update(order)


@app.get('/get_product/{product_id}')
async def get_product(product_id: int):
    d = {"product_id": product_id}
    product_meta = ProductMeta(**d)
    return _get(product_meta)


@app.delete('/delete_product/{product_id}')
async def delete_product(product_id: int):
    d = {"product_id": product_id}
    product_meta = ProductMeta(**d)
    return _delete(product_meta)


@app.post('/add_product')
async def add_product(product: Product):
    product.product_id = None
    return _add(product)
    
@app.put('/update_product')
async def update_product(product: Product):
    return _update(product)


def _get(obj):
    sql = sq.select_sql(obj)
    return _get_db().sql_to_json(sql)


def _delete(obj):
    sql = sq.delete_sql(obj)
    return _execute(sql)


def _add(obj):
    sql = sq.insert_sql(obj)
    return _execute(sql)


def _update(obj):
    sql = sq.update_sql(obj)
    return _execute(sql)


def _execute(sql):
    return _get_db().execute_sql(sql)


def _get_db():
    return pg.PostgresUtil()
