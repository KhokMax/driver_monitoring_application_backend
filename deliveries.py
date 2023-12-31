import pandas as pd
import uuid
import json
from flask import request
from flask_restful import Resource
from sqlalchemy import create_engine, text, exc, pool
from  queries import *

class Deliveries(Resource):

    def post(self):
        try:
            delivery_id = str(uuid.uuid4())

            column_list = ["delivery_id", 'delivery_name', 'delivery_description', 'deadline', 'shipfrom_longitude', 'shipfrom_latitude',
                           'shipto_longitude', 'shipto_latitude', 'shipto_address', 'shipfrom_address', 'vehicle_id', 'driver_id']

            values = [delivery_id if item == "delivery_id" else request.json.get(item, None) for item in column_list]
            sql_query = f"INSERT INTO deliveries ({', '.join(column_list)}) VALUES ({', '.join(':' + item for item in column_list)})"

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

    
    def get_all(self):
        try:
            engine = create_engine("postgresql+psycopg2://avnadmin:AVNS_zb-76Zov-eh6OfnbW-Z@driver-monitoring-application-db-khok-8eb3.a.aivencloud.com:19713/defaultdb", poolclass=pool.QueuePool)
            connection = engine.connect()
            
            df = pd.read_sql(get_all_deliveries, connection)
            
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


    def get(self, driver_id=None):
            
            if driver_id == None:
                return self.get_all()

            try:
                engine = create_engine("postgresql+psycopg2://avnadmin:AVNS_zb-76Zov-eh6OfnbW-Z@driver-monitoring-application-db-khok-8eb3.a.aivencloud.com:19713/defaultdb", poolclass=pool.QueuePool)
                connection = engine.connect()
                
                df = pd.read_sql(get_all_deliveries_by_driver.format(driver_id), connection)
                
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
        