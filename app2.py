#!/usr/bin/python
import json
from webapp.bdtools import bdtools
from flask import Flask,jsonify
from flask_cors import CORS
from flask_restful import Resource, Api



app = Flask(__name__)
CORS(app)
api = Api(app)



class Services(Resource):
    def get(self):
        #conn = db_connect.connect()  # connect to database
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

        #querybd = conn.execute("select * from politician")  # This line performs query and returns json result
        #print (jsonify(query))
        #return {'employees': [i[1] for i in querybd.cursor.fetchall()]}  # Fetches first column that is Employee ID

        bdtools.updatePolitician()
        data = bdtools.getData()
        #return jsonify(data.get(1))
        return jsonify(bdtools.updatePolitician())



api.add_resource(Services, '/politicians')  # Route_1


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

def createJson():
    data = {}
    data['attr'] = {"id": "t1",
                    "name": "Wibeu",
                    "superiorid": "Wibeu",
                    "subordinateid": "Curusego",
                    }
    json_data = json.dumps(data)





if __name__ == '__main__':
    #bdtools.updateData()
    #app.run(debug=True)
    app.run(host=app.config['TRANSLATE_HOST'], port=int(app.config['TRANSLATE_PORT']))
