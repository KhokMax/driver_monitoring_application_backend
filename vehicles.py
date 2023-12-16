import pandas as pd
import uuid
from flask import request
from flask_restful import Resource
from sqlalchemy import create_engine, text, exc
from  queries import *

class Vehicles(Resource):

    def post(self):
        try:
            vehicle_id = str(uuid.uuid4())

            column_list = ["vehicle_id", "vehicle_name", "max_distance", "fuel_per_100_km", "capacity_kg", "license_category", "vehicle_category"]

            values = [vehicle_id if item == "vehicle_id" else request.json.get(item, None) for item in column_list]
        except Exception as e:
            print(e)
            return {"Exeption": "404"}


        try:
            engine = create_engine("postgresql+psycopg2://avnadmin:AVNS_zb-76Zov-eh6OfnbW-Z@driver-monitoring-application-db-khok-8eb3.a.aivencloud.com:19713/defaultdb")
            connection = engine.connect()

            sql_query = f"INSERT INTO VEHICLES ({', '.join(column_list)}) VALUES ({', '.join(':' + item for item in column_list)})"
            connection.execute(text(sql_query), dict(zip(column_list, values)))

            connection.commit()
            connection.close()

        except exc.IntegrityError:
            connection.rollback()
            connection.close()
            return {"Exeption": "data error"}
        
        except Exception as e:
            print(e)
            connection.rollback()
            connection.close()
            return {"Exeption": "404"}
        
        return {"Response": "200"}
    

    def delete(self, vehicle_id):
        try:
            engine = create_engine("postgresql+psycopg2://avnadmin:AVNS_zb-76Zov-eh6OfnbW-Z@driver-monitoring-application-db-khok-8eb3.a.aivencloud.com:19713/defaultdb")
            connection = engine.connect()

            sql_query = f"UPDATE VEHICLES SET alive_flag = false WHERE vehicle_id = '{str(vehicle_id)}'"
            connection.execute(text(sql_query))

            connection.commit()
            connection.close()

        except Exception as e:
            print(e)
            return {"Exeption": "404"}
        
        return {"Response": "200"}
    
    def get(self):
        try:
            engine = create_engine("postgresql+psycopg2://avnadmin:AVNS_zb-76Zov-eh6OfnbW-Z@driver-monitoring-application-db-khok-8eb3.a.aivencloud.com:19713/defaultdb")
            connection = engine.connect()
            df = pd.read_sql(select_all_vehicles, connection)
        except Exception as e:
            print(e)
            return {"Exeption": "404"}
        
        return df.to_json(orient="index")