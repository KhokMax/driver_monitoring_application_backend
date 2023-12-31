from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS
import pandas as pd
from sqlalchemy import create_engine
from  queries import *
from  drivers import *
from  vehicles import *
from  deliveries import *
from  users import *
from  operations import *
from vehicle_location import *



# app = Flask(__name__)
# api = Api()
app = Flask(__name__)
api = Api(app)  # Передайте екземпляр вашого Flask застосунку в конструктор Api
CORS(app, origins="*")  # Використовуйте CORS для вашого застосунку


class Main(Resource):
    def get(self):
        engine = create_engine("postgresql+psycopg2://avnadmin:AVNS_zb-76Zov-eh6OfnbW-Z@driver-monitoring-application-db-khok-8eb3.a.aivencloud.com:19713/defaultdb")
        connection = engine.connect()
        df = pd.read_sql(get_all_deliveries, connection)
        return df.to_json(orient="index")

api.add_resource(Main, "/main")
api.add_resource(Drivers, "/driver", "/driver/<user_id>", "/drivers")
api.add_resource(Vehicles, "/vehicle", "/vehicle/<vehicle_id>", "/vehicles")
api.add_resource(Deliveries, "/delivery", "/deliveries", "/deliveries/<driver_id>")
api.add_resource(Users, "/user/<login>,<password>")
api.add_resource(Operations, "/operation/delivery/delivery_id=<delivery_id>,status=<status>")
api.add_resource(Location, "/location", "/location/<vehicle_id>")

# api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
