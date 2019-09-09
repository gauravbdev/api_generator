import configparser
import pandas as pd
import schema_sql as ss
import inflect
import psycopg2


conf_templ = """
# singular : is singular noun, this is how class names will be created in the api/model
# allow : enable API operations as needed
# insert_pk : set false if pk is an auto-increment/serial column

# standard 

{}


"""

table_templ = """
    [{}]
    singular: {}
    allow: insert,select,update,delete
    insert_pk: {} 

"""

no_pk_templ = """
    # [{}]
    # excluded, no primary key found

"""

def generate(conn, sql):
    df = pd.read_sql(sql, conn)
    tables_str = ''
    lines_sep = '\n\n'
    inf = inflect.engine()
    for index, row in df.iterrows():
        table = row['table_name'].lower().replace(' ', '_')
        infout = inf.singular_noun(table)
        singular = table if not infout else infout
        insert_pk = 'true' if row['insert_pk'] == 1 else 'false'
        if row['has_pk'] == 1:
            ts = table_templ.format(table, singular, insert_pk)
        else:
            ts = no_pk_templ.format(table)
        tables_str = tables_str + ts
    conf = conf_templ.format(tables_str)
    return conf



def main():
    config = configparser.ConfigParser()
    config.read('settings.conf')
    conn_str = config['db']['conn_string']
    conn = psycopg2.connect(conn_str)
    table_schema = config['db']['table_schema']
    sql = ss.pg_schema_tables_sql
    sql = sql.format(sql, table_schema=table_schema)
    code = generate(conn, sql)
    out_file = 'api_gen.conf'
    with open(out_file, 'w') as text_file:
        text_file.write(code)
    print(str.format("Success! generated conf saved : {}", out_file))


if __name__ == '__main__':
    main()
