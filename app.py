from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
# from flask.ext.jsonpify import jsonify

db_connect = create_engine('sqlite:///chinook.db')
app = Flask(__name__)
CORS(app)
api = Api(app)
conn = db_connect.connect()  # connect to database


class Employees(Resource):
    def get(self):
        query = [{"attr": {"id": "t1",
                           "name": "Wibeu",
                           "superiorid": "Wibeu",
                           "subordinateid": "Curusego",
                           },
                  "children": [
                      {"attr": {"id": "t1:1",
                                "name": "Curusego",
                                "superiorid": "Wibeu",
                                "subordinateid": "Nalvar",
                                },
                       "children": [
                           {"attr": {"id": "t1:1:1",
                                     "name": "Nalvar",
                                     "superiorid": "Curusego",
                                     "subordinateid": "",
                                     }
                            },
                           {"attr": {"id": "t1:1:2",
                                     "name": "Bufiobere",
                                     "superiorid": "Curusego",
                                     "subordinateid": "",
                                     }
                            }
                       ]
                       },
                      {"attr": {"id": "t1:2",
                                "name": "Flunodae",
                                "superiorid": "Wibeu",
                                "subordinateid": "Osceo",
                                },
                       "children": [
                           {"attr": {"id": "t1:2:1",
                                     "name": "Osceo",
                                     "superiorid": "Flunodae",
                                     "subordinateid": "",
                                     }
                            }
                       ]
                       },
                      {"attr": {"id": "t1:3",
                                "name": "Envailslag",
                                "superiorid": "Wibeu",
                                "subordinateid": "",
                                }
                       }
                  ]
                  }, ]
        querybd = conn.execute("select * from employees")  # This line performs query and returns json result
        print jsonify(querybd)
        #return {'employees': [i[0] for i in query.cursor.fetchall()]}  # Fetches first column that is Employee ID
        return jsonify(query)


api.add_resource(Employees, '/employees')  # Route_1


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

if __name__ == '__main__':
    app.run(debug=True)
