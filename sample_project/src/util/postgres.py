import configparser
import psycopg2
import json
import pandas as pd


class PostgresUtil(object):
    def __init__(self):
        conf_path = 'settings.conf'
        config = configparser.ConfigParser()
        config.read(conf_path)
        conn_str = config['db']['conn_string']
        try:
            self._set_session(conn_str)
        except Exception as e:
            print('Error connecting to db server. ', str(e))


    def _set_session(self, conn_str):
        self.conn = psycopg2.connect(conn_str)


    def _sql_to_df(self, query):
        return pd.read_sql(query, self.conn)

    
    def sql_to_json(self, query):
        return self._sql_to_df(query).to_dict(orient='records')


    def execute_sql(self, query):
        response = {"is_success": False, "msg": ""}
        try:
            cur = self.conn.cursor()
            cur.execute(query)
            returning_id = cur.fetchone()[0]
            self.conn.commit()
            cur.close()
            response["is_success"] = True
            action = query.split(' ')[0]
            msg = str.format("{} done", action)
            response["id"] = returning_id
            response["msg"] = msg
        except Exception as e:
            response["msg"] = str(e)
        return response

    
    def __del__(self):
        self.conn.close()
