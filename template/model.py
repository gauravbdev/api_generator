template = """

from pydantic import BaseModel


class {class_name}Meta(BaseModel):
{declare_pks}
    class Info():
        table = '{table}'
        pk = {pk_list}


class {class_name}({class_name}Meta):
{declare_columns}
"""

