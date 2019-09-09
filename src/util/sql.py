
def select_sql(meta_obj):
    sql = "SELECT * FROM {} WHERE {};"
    table = meta_obj.Info.table
    pkvs = _get_kv_str(meta_obj, " and", True)
    sql = sql.format(table, pkvs)
    return sql


def delete_sql(meta_obj):
    sql = "DELETE FROM {} WHERE {} RETURNING {};"
    table = meta_obj.Info.table
    pkvs = _get_kv_str(meta_obj, " and", True)
    pks = ', '.join(meta_obj.Info.pk)
    sql = sql.format(table, pkvs, pks)
    return sql



def insert_sql(model_obj):
    sql = "INSERT INTO {}({})  VALUES({}) RETURNING {};"
    d = model_obj.__values__
    exclude = []
    for k, v in d.items():
        if v is None:
            exclude.append(k)
    for exc in exclude:
        del d[exc]
    table = model_obj.Info.table
    fields = ', '.join(list(d.keys()))
    values = str(list(d.values()))[1:-1]
    pks = ', '.join(model_obj.Info.pk)
    sql = sql.format(table, fields, values, pks)
    return sql


def update_sql(model_obj):
    sql = "UPDATE {} SET {} WHERE {} RETURNING {}"
    table = model_obj.Info.table
    kvs = _get_kv_str(model_obj)
    pkvs = _get_kv_str(model_obj, " and", True)
    pks = ', '.join(model_obj.Info.pk)
    sql = sql.format(table, kvs, pkvs, pks)
    return sql



def _get_kv_str(model_obj, sep=",", pk_only=False):
    d = model_obj.__values__
    kv_list = []
    for key, value in d.items():
        if key == "table":
            continue
        encl = "" if type(d[key]) in [int, float] else "'"
        kv_str = str.format("{}={}{}{}", key, encl, value, encl)
        if pk_only and key in model_obj.Info.pk:
            kv_list.append(kv_str) 
        if not pk_only and key not in model_obj.Info.pk:
            kv_list.append(kv_str) 
    sep = sep + " "
    return sep.join(kv_list)


