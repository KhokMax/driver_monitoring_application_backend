import pandas as pd
import uuid
import json
from flask import request
from flask_restful import Resource
from sqlalchemy import create_engine, text, exc, pool
from  queries import *

class Operations(Resource):

    def post(self, delivery_id, status):
        try:

            if status not in ['End', 'In progress']:
                print(status)
                return {"Exception": "404", "Description": "Database interaction error"}

            engine = create_engine("postgresql+psycopg2://avnadmin:AVNS_zb-76Zov-eh6OfnbW-Z@driver-monitoring-application-db-khok-8eb3.a.aivencloud.com:19713/defaultdb", poolclass=pool.QueuePool)
            connection = engine.connect()

            connection.execute(text(change_delivery_status.format(status, delivery_id)))
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