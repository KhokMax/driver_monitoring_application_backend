import pandas as pd
import uuid
import json
from flask import request
from flask_restful import Resource
from sqlalchemy import create_engine, text, exc, pool
from queries import select_all_drivers

class Drivers(Resource):

    def create_user(self, login, password, connection):
        user_id = str(uuid.uuid4())
        sql_query = "INSERT INTO users (user_id, login, user_password) VALUES (:user_id, :login, :user_password)"
        connection.execute(text(sql_query), {'user_id': user_id, 'login': login, 'user_password': password})
        return user_id


    def post(self):
        try:
            login = request.json.get('login', None)
            password = request.json.get('password', None)

            with create_engine("postgresql+psycopg2://avnadmin:AVNS_zb-76Zov-eh6OfnbW-Z@driver-monitoring-application-db-khok-8eb3.a.aivencloud.com:19713/defaultdb").connect() as connection:
                try:
                    user_id = self.create_user(login, password, connection)

                    column_list = ['driver_first_name', 'driver_last_name', 'driver_patronymic',
                                    'driver_age', 'driver_rank', 'mobile_phone', 'mail', 'a1_category',
                                    'a_category', 'b1_category', 'b_category', 'c1_category', 'c_categoty',
                                    'd1_categoty', 'd_category', 'c1e_category', 'be_category', 'ce_category',
                                    'd1e_category', 'de_category', "user_id"]

                    values = [user_id if item == "user_id" else request.json.get(item, None) for item in column_list]
                    sql_query = f"INSERT INTO drivers ({', '.join(column_list)}) VALUES ({', '.join(':' + item for item in column_list)})"

                    connection.execute(text(sql_query), dict(zip(column_list, values)))
                    connection.commit()
                except Exception as e:
                    connection.rollback()
                    print(e)
                    return {"Exception": "404", "Description": "Database interaction error"}
        
        except Exception as e:
            print(e)
            return {"Exception": "404"}
        
        return {"Response": "200"}


    def delete(self, user_id):
        try:

            sql_query = f"UPDATE DRIVERS SET alive_flag = false WHERE user_id = '{str(user_id)}'"

            with create_engine("postgresql+psycopg2://avnadmin:AVNS_zb-76Zov-eh6OfnbW-Z@driver-monitoring-application-db-khok-8eb3.a.aivencloud.com:19713/defaultdb").connect() as connection:
                try:
                    connection.execute(text(sql_query))
                    connection.commit()
                except Exception as e:
                    connection.rollback()
                    print(e)
                    return {"Exception": "404", "Description": "Database interaction error"}

        except Exception as e:
            print(e)
            return {"Exception": "404"}
        
        return {"Response": "200"}


    def get(self):
        try:
            engine = create_engine("postgresql+psycopg2://avnadmin:AVNS_zb-76Zov-eh6OfnbW-Z@driver-monitoring-application-db-khok-8eb3.a.aivencloud.com:19713/defaultdb", poolclass=pool.QueuePool)
            connection = engine.connect()
            
            df = pd.read_sql(select_all_drivers, connection)
            
            data = json.loads(df.to_json(orient="records"))
            result_json_str = json.dumps({"drivers": data}) 
            connection.close()
            engine.dispose(False)    
        except Exception as e:
            print(e)
            return {"Exception": "404"}
         
        return result_json_str