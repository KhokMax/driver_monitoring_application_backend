import pandas as pd
import uuid
import json
from flask import request
from flask_restful import Resource
from sqlalchemy import create_engine, text, exc, pool
from  queries import *

class Location(Resource):

    def post(self):
        try:
            delivery_id = str(uuid.uuid4())

            column_list = ['vehicle_id', 'longitude', 'latitude']

            values = [request.json.get(item, None) for item in column_list]
            sql_query = f"INSERT INTO VEHICLE_LOCATIONS ({', '.join(column_list)}) VALUES ({', '.join(':' + item for item in column_list)})"

            engine = create_engine("postgresql+psycopg2://avnadmin:AVNS_zb-76Zov-eh6OfnbW-Z@driver-monitoring-application-db-khok-8eb3.a.aivencloud.com:19713/defaultdb", poolclass=pool.QueuePool)
            connection = engine.connect()
                
            connection.execute(text(sql_query), dict(zip(column_list, values)))
            connection.commit()

            connection.close()
            engine.dispose()
        
        except Exception as e:
            try:
                connection.rollback()
                connection.close()
                engine.dispose()
            except Exception as e:
                print(e)
                return {"Exception": "404"}
            
            print(e)
            return {"Exception": "404", "Description": "Database interaction error"}
        
        return {"Response": "200"}

    
    def get(self, vehicle_id):
        try:
            engine = create_engine("postgresql+psycopg2://avnadmin:AVNS_zb-76Zov-eh6OfnbW-Z@driver-monitoring-application-db-khok-8eb3.a.aivencloud.com:19713/defaultdb", poolclass=pool.QueuePool)
            connection = engine.connect()
            
            df = pd.read_sql(select_last_vehicle_location.format(vehicle_id), connection)
            
            data = json.loads(df.to_json(orient="records"))
            result_json_str = json.dumps({"deliveries": data})

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