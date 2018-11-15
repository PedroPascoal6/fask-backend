# coding=utf-8
# Set the settings file to the local version and run the app.
import os
from webapp import factory
from webapp.views import services
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse

os.environ['APP_SETTINGS_FILE'] = 'settings/local.py'

app = factory.create_app()
CORS(app)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('politicianid', type=int)
parser.add_argument('jail', type=bool)


class Services(Resource):
    def get(self):
        return services.dosomething()

    def post(self):
        args = parser.parse_args()
        politician_id = str(args['politicianid'])
        jail = args['jail']
        services.createEvent(politician_id, jail)
        return {"success": 'true'}


api.add_resource(Services, '/politicians')  # Route_1


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


if __name__ == '__main__':
    app.run(debug=True)
