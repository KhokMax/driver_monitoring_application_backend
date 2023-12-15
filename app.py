from flask import Flask
from flask_restful import Api, Resource
import pandas as pd
from sqlalchemy import create_engine
from  queries import *
from  drivers import *

app = Flask(__name__)
api = Api()

# conn = psycopg2.connect(host="34.168.253.165", port="5432", dbname="postgres", password="IvNa2023OlKh", user="postgres")
# cursor = conn.cursor()



class Main(Resource):
    def get(self):
        engine = create_engine("postgresql+psycopg2://avnadmin:AVNS_zb-76Zov-eh6OfnbW-Z@driver-monitoring-application-db-khok-8eb3.a.aivencloud.com:19713/defaultdb")
        connection = engine.connect();
        df = pd.read_sql(get_all_deliveries, connection);
        return df.to_json(orient="index")
        #return "ewfewfwe"

api.add_resource(Main, "/main")
api.add_resource(Drivers, "/driver", "/driver/<user_id>")
api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
