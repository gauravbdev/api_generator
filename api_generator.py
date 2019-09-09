import configparser
import schema_sql as ss
from template import model as mt
from template import app as at
import pandas as pd
import schema_sql as ss
import psycopg2
import os
from shutil import rmtree
from shutil import copyfile


def get_attributes(config, key):
    singular = config[key]['singular']
    ops_allowed = config[key]['allow'].split(',')
    #insert_pk = config[key]['insert_pk']
    insert_pk = config.getboolean(key, 'insert_pk')
    return singular, ops_allowed, insert_pk


def get_pk_list(df):
    return df[df['is_pk'] == 1]['column_name'].tolist()


def get_cols(df, is_pk):
    df = df[df['is_pk'] == is_pk]
    cols = ''
    for idx, row in df.iterrows():
        col = '{}: {}'.format(row['column_name'], 
                                row['datatype'])
        cols = cols + '    ' + col + '\n'
    return cols
        

def update_datatype(df):
    for idx, row in df.iterrows():
        dtype = row['datatype']
        if 'int' in dtype:
            df.at[idx, 'datatype'] = 'int'
        elif 'numeric' in dtype \
                or 'float' in dtype \
                or 'real' in dtype:
            df.at[idx, 'datatype'] = 'float'
        else: 
            df.at[idx, 'datatype'] = 'str'
    return df

 
def generate_model(tdf, table, singular, pk_list):
    pk_list_str = str(pk_list)
    declare_columns = get_cols(tdf, 0)
    declare_pks = get_cols(tdf, 1)
    class_name = singular.capitalize()
    model_code = mt.template.format(class_name=class_name, 
                    declare_pks=declare_pks, table=table,
                    declare_columns=declare_columns,
                    pk_list = pk_list)
    filename = 'src/model/{}.py'.format(singular)
    save_to_file(filename, model_code)


def save_to_file(filename, text):
    with open(filename, 'w') as text_file:
        text_file.write(text)


def get_app_code(tdf, table, singular, ops_allowed, 
                    insert_pk, pk_list):
    # TODO : add logic for multiple pks
    if len(pk_list) > 1:
        return '', ''
    pk = pk_list[0]
    pk_dtype = get_cols(tdf, 1).strip()
    class_name = singular.capitalize()
    method_code = ''
    import_code = at.import_code.format(singular=singular)
    set_pk_none = ''
    if not insert_pk:
        set_pk_none = at.set_pk_none.format(singular=singular, pk=pk)
    if 'select' in ops_allowed:
        method_code += at.get_method.format(singular=singular, pk=pk, 
                pk_dtype=pk_dtype, class_name=class_name)
    if 'delete' in ops_allowed:
        method_code += at.delete_method.format(singular=singular, pk=pk, 
                pk_dtype=pk_dtype, class_name=class_name)
    if 'insert' in ops_allowed:
        method_code += at.add_method.format(singular=singular, pk=pk, 
                class_name=class_name, set_pk_none=set_pk_none)
    if 'update' in ops_allowed:
        method_code += at.update_method.format(singular=singular,
                class_name=class_name)
    return method_code, import_code


def generate_code(df, config):
    method_code = ''
    import_code = ''
    for table in list(config.keys()):
        tdf = df[df['table_name'] == table]
        if table == 'DEFAULT':
            continue
        singular, ops_allowed, insert_pk = get_attributes(config, table)
        pk_list = get_pk_list(tdf)
        generate_model(tdf, table, singular, pk_list)
        # generate app :
        mcode, icode = get_app_code(tdf, table, singular, 
                ops_allowed, insert_pk, pk_list)
        method_code += mcode
        import_code += icode
    app_code = at.app_code.format(import_code=import_code, 
            method_code=method_code)
    save_to_file('src/app.py', app_code)


def clear_model():
    folder = 'src/model'
    rmtree(folder, ignore_errors=True)
    os.makedirs(folder)


def main():
    api_gen_conf = 'api_gen.conf'
    if not os.path.isfile(api_gen_conf):
        print("api_gen.conf not generated, " +
                "run python3 conf_generator.py first")
        return
    config = configparser.ConfigParser()
    settings_file = 'settings.conf'
    config.read(settings_file)
    conn_str = config['db']['conn_string']
    conn = psycopg2.connect(conn_str)
    table_schema = config['db']['table_schema']
    sql = ss.pg_schema_cols_sql
    sql = sql.format(sql, table_schema=table_schema)
    config = configparser.ConfigParser()
    config.read('api_gen.conf')
    df = pd.read_sql(sql, conn)
    df = update_datatype(df)
    clear_model()
    generate_code(df, config)
    copyfile(settings_file,  'src/{}'.format(settings_file))
    print("Success! API code has been generated.")


if __name__ == '__main__':
    main()

