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


class Employees(Resource):
    def get(self):
        query = [{"attr": {"id": "t1",
                           "name": "Task 1",
                           "resource": "Chadwick",
                           "start": "1/1/2014",
                           "end": "10/1/2014"
                           },
                  "children": [
                      {"attr": {"id": "t1:1",
                                "name": "Task 1-1",
                                "resource": "Chris",
                                "start": "1/1/2014",
                                "end": "3/1/2014"
                                },
                       "children": [
                           {"attr": {"id": "t1:1:1",
                                     "name": "Task 1-1-1",
                                     "resource": "Henry",
                                     "start": "1/1/2014",
                                     "end": "2/1/2014"
                                     }
                            },
                           {"attr": {"id": "t1:1:2",
                                     "name": "Task 1-1-2",
                                     "resource": "Victor",
                                     "start": "2/1/2014",
                                     "end": "3/1/2014"
                                     }
                            }
                       ]
                       },
                      {"attr": {"id": "t1:2",
                                "name": "Task 1-2",
                                "resource": "Jim",
                                "start": "3/1/2014",
                                "end": "6/1/2014"
                                },
                       "children": [
                           {"attr": {"id": "t1:2:1",
                                     "name": "Task 1-2-1",
                                     "resource": "Jay",
                                     "start": "3/1/2014",
                                     "end": "5/1/2014"
                                     }
                            },
                           {"attr": {"id": "t1:2:2",
                                     "name": "Task 1-2-2",
                                     "resource": "Karin",
                                     "start": "5/1/2014",
                                     "end": "6/1/2014"
                                     }
                            }
                       ]
                       },
                      {"attr": {"id": "t1:3",
                                "name": "Task 1-3",
                                "resource": "Chadwick",
                                "start": "6/1/2014",
                                "end": "8/1/2014"
                                }
                       },
                      {"attr": {"id": "t1:4",
                                "name": "Task 1-4",
                                "resource": "Chris",
                                "start": "8/1/2014",
                                "end": "10/1/2014"
                                }
                       }
                  ]
                  }, ]
        # query = conn.execute("select * from employees")  # This line performs query and returns json result
        #return {'employees': [i[0] for i in query.cursor.fetchall()]}  # Fetches first column that is Employee ID
        return jsonify(query)
        conn = db_connect.connect()  # connect to database

api.add_resource(Employees, '/employees')  # Route_1


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

if __name__ == '__main__':
    app.run()
