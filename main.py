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
        engine = create_engine("postgresql+psycopg2://postgres:IvNa2023OlKh@34.168.253.165:5432/postgres")
        connection = engine.connect();
        df = pd.read_sql(get_all_deliveries, connection);
        return df.to_json(orient="index")

api.add_resource(Main, "/main")
api.add_resource(Drivers, "/driver", "/driver/<user_id>")
api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True, port=3000, host='127.0.0.1')
