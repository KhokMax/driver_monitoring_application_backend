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
            sql_query = f"INSERT INTO VEHICLES ({', '.join(column_list)}) VALUES ({', '.join(':' + item for item in column_list)})"

            with create_engine("postgresql+psycopg2://avnadmin:AVNS_zb-76Zov-eh6OfnbW-Z@driver-monitoring-application-db-khok-8eb3.a.aivencloud.com:19713/defaultdb").connect() as connection:
                try:
                    connection.execute(text(sql_query), dict(zip(column_list, values)))
                    connection.commit()
                except Exception as e:
                    connection.rollback()
                    print(e)
                    return {"Exception": "404", "Description": "Database interaction error"}
        
        except Exception as e:
            print(e)
            return {"Exeption": "404"}
        
        return {"Response": "200"}
    

    def delete(self, vehicle_id):
        try:
            sql_query = f"UPDATE VEHICLES SET alive_flag = false WHERE vehicle_id = '{str(vehicle_id)}'"

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
            return {"Exeption": "404"}
        
        return {"Response": "200"}
    

    def get(self):
        try:
            with create_engine("postgresql+psycopg2://avnadmin:AVNS_zb-76Zov-eh6OfnbW-Z@driver-monitoring-application-db-khok-8eb3.a.aivencloud.com:19713/defaultdb").connect() as connection:
                df = pd.read_sql(select_all_vehicles, connection)
        except Exception as e:
            print(e)
            return {"Exeption": "404"}
        
        return {'"vehicles"': df.to_json(orient="records")}