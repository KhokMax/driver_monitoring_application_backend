import pandas as pd
import uuid
from flask import request
from flask_restful import Resource
from sqlalchemy import create_engine, text, exc
from  queries import *

class Deliveries(Resource):

    def post(self):
        try:
            delivery_id = str(uuid.uuid4())

            column_list = ["delivery_id", 'delivery_name', 'delivery_description', 'deadline', 'shipfrom_longitude', 'shipfrom_latitude',
                           'shipto_longitude', 'shipto_latitude', 'shipto_address', 'shipfrom_address', 'vehicle_id', 'driver_id']

            values = [delivery_id if item == "delivery_id" else request.json.get(item, None) for item in column_list]
        except Exception as e:
            print(e)
            return {"Exeption": "404"}


        try:
            engine = create_engine("postgresql+psycopg2://avnadmin:AVNS_zb-76Zov-eh6OfnbW-Z@driver-monitoring-application-db-khok-8eb3.a.aivencloud.com:19713/defaultdb")
            connection = engine.connect()

            sql_query = f"INSERT INTO deliveries ({', '.join(column_list)}) VALUES ({', '.join(':' + item for item in column_list)})"
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
    
    
    def get(self):

        try:
            engine = create_engine("postgresql+psycopg2://avnadmin:AVNS_zb-76Zov-eh6OfnbW-Z@driver-monitoring-application-db-khok-8eb3.a.aivencloud.com:19713/defaultdb")
            connection = engine.connect()
            df = pd.read_sql(get_all_deliveries, connection)
            connection.close()
        except Exception as e:
            print(e)
            return {"Exeption": "404"}
        
        return {"deliveries": df.to_json(orient="records")}

        