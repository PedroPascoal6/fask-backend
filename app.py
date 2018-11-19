# coding=utf-8
# Set the settings file to the local version and run the app.
import os
from webapp import factory
from webapp.views import services
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from webapp.models import generate_data

os.environ['APP_SETTINGS_FILE'] = 'settings/local.py'

app = factory.create_app()
CORS(app)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('politicianid', type=int)
parser.add_argument('jail', type=bool)
parser.add_argument('amount', type=int)


class Services(Resource):
    def get(self):
        return services.get_data()

    def post(self):
        args = parser.parse_args()
        politician_id = str(args['politicianid'])
        jail = args['jail']
        services.createEvent(politician_id, jail)
        return {"success": 'true'}


class Support(Resource):
    def post(self):
        args = parser.parse_args()
        amount = args['amount']
        generate_data(amount)
        return {"success": 'true'}


api.add_resource(Services, '/politicians')  # Route_1
api.add_resource(Support, '/support')  # Route_2


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


if __name__ == '__main__':
    app.run(debug=True)
