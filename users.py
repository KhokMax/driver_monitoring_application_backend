import pandas as pd
import json
from flask_restful import Resource
from sqlalchemy import create_engine, pool


class Users(Resource):


    def get(self, login, password):
        try:
            engine = create_engine("postgresql+psycopg2://avnadmin:AVNS_zb-76Zov-eh6OfnbW-Z@driver-monitoring-application-db-khok-8eb3.a.aivencloud.com:19713/defaultdb", poolclass=pool.QueuePool)
            connection = engine.connect()
            
            sql_query = f"SELECT * FROM users WHERE login = '{str(login)}' and user_password = '{password}'"

            df = pd.read_sql(sql_query, connection)
            
            data = json.loads(df.to_json(orient="records"))
            result_json_str = json.dumps({"user": data})

            connection.close()
            engine.dispose()

        except Exception as e:
            try:
                connection.close()
                engine.dispose()
            except Exception as e:
                print(e)
                return {"Exception": "404"}
            
            print(e)
            return {"Exception": "404"}
         
        return result_json_str