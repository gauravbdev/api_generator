app_code = """
from fastapi import FastAPI
from util import sql as sq
from util import postgres as pg
import json
{import_code}

app = FastAPI(docs_url='/')
{method_code}

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
"""


import_code = """
from model.{singular} import *"""


get_method = """

@app.get('/get_{singular}/{{{pk}}}')
async def get_{singular}({pk_dtype}):
    d = {{"{pk}": {pk}}}
    {singular}_meta = {class_name}Meta(**d)
    return _get({singular}_meta)
"""

delete_method = """

@app.delete('/delete_{singular}/{{{pk}}}')
async def delete_{singular}({pk_dtype}):
    d = {{"{pk}": {pk}}}
    {singular}_meta = {class_name}Meta(**d)
    return _delete({singular}_meta)
"""


add_method = """

@app.post('/add_{singular}')
async def add_{singular}({singular}: {class_name}):
    {set_pk_none}
    return _add({singular})
"""

set_pk_none = """{singular}.{pk} = None"""


update_method = """    
@app.put('/update_{singular}')
async def update_{singular}({singular}: {class_name}):
    return _update({singular})
"""
