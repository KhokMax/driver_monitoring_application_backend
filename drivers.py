import pandas as pd
import uuid
import psycopg2
from flask import request
from flask_restful import Resource
from sqlalchemy import create_engine, text, exc
from  queries import *

class Drivers(Resource):

    def create_user(self, login, password):
        engine = create_engine("postgresql+psycopg2://avnadmin:AVNS_zb-76Zov-eh6OfnbW-Z@driver-monitoring-application-db-khok-8eb3.a.aivencloud.com:19713/defaultdb")
        connection = engine.connect()
        sql_query = f"INSERT INTO users (user_id, login, user_password) VALUES (:user_id, :login, :user_password)"
        user_id = str(uuid.uuid4())
        connection.execute(text(sql_query), {'user_id': user_id, 'login':login, 'user_password': password})

        connection.commit()
        connection.close()

        return user_id

        

    def post(self):
        try:
            login = request.json.get('login', None)
            password = request.json.get('password', None)

            user_id = self.create_user(login, password)

            column_list = ['driver_first_name', 'driver_last_name', 'driver_patronymic',
                            'driver_age', 'driver_rank', 'mobile_phone', 'mail', 'a1_category',
                            'a_category', 'b1_category', 'b_category', 'c1_category', 'c_categoty',
                            'd1_categoty', 'd_category', 'c1e_category', 'be_category', 'ce_category',
                            'd1e_category', 'de_category', "user_id"]

            values = [user_id if item == "user_id" else request.json.get(item, None) for item in column_list]
        except:
            connection.rollback()
            connection.close()
            return {"Exeption": "404"}


        try:
            engine = create_engine("postgresql+psycopg2://avnadmin:AVNS_zb-76Zov-eh6OfnbW-Z@driver-monitoring-application-db-khok-8eb3.a.aivencloud.com:19713/defaultdb")
            connection = engine.connect()

            sql_query = f"INSERT INTO drivers ({', '.join(column_list)}) VALUES ({', '.join(':' + item for item in column_list)})"
            connection.execute(text(sql_query), dict(zip(column_list, values)))

            connection.commit()
            connection.close()

        except exc.IntegrityError:
            connection.rollback()
            connection.close()
            return {"Exeption": "data error"}
        
        except:
            connection.rollback()
            connection.close()
            return {"Exeption": "404"}
        
        return {"Response": "200"}
    

    def delete(self, user_id):
        print("dewdewdewdew")
        
        try:
            engine = create_engine("postgresql+psycopg2://postgres:IvNa2023OlKh@34.168.253.165:5432/postgres")
            connection = engine.connect()

            sql_query = f"DELETE FROM users WHERE user_id = '{user_id}'"
            connection.execute(text(sql_query))

            connection.commit()
            connection.close()

        except:
            return {"Exeption": "404"}
        
        return {"Response": "200"}
    
    
    def delete(self, user_id):
        
        try:
            engine = create_engine("postgresql+psycopg2://postgres:IvNa2023OlKh@34.168.253.165:5432/postgres")
            connection = engine.connect()

            sql_query = f"DELETE FROM users WHERE user_id = '{user_id}'"
            connection.execute(text(sql_query))

            connection.commit()
            connection.close()

        except:
            return {"Exeption": "404"}
        
        return {"Response": "200"}