#!/usr/bin/python
import sqlite3
from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Resource, Api
from sqlalchemy import create_engine
import json
import sqlite3
from json import dumps
# from flask.ext.jsonpify import jsonify

db_connect = create_engine('sqlite:///politiciansBD.db')
app = Flask(__name__)
CORS(app)
api = Api(app)



class Employees(Resource):
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

        con = sqlite3.connect("politiciansBD.db")
        # Print the table contents
        data={}
        for row in con.execute("select * from politician"):
            data[row[0]] = {"name": row[1],
                            "superiorid": row[2],
                            "superiorName": row[3],
                            "subordinateid": row[4],
                            "subordinateName": row[5]}
        print (data)



        return jsonify(data)



api.add_resource(Employees, '/employees')  # Route_1


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


def updateData():
    conn = db_connect.connect()  # connect to database

    sql = ''' INSERT INTO politician VALUES(0,'Wibeu',null,'',1,'Curusego',1) '''
    conn.execute(sql)
    sql = ''' INSERT INTO politician VALUES(1,'Curusego',1,'Curusego',2,'Nalvar',1) '''
    conn.execute(sql)
    sql = ''' INSERT INTO politician VALUES(2,'Nalvar',1,'Curusego',null,'',1) '''
    conn.execute(sql)
    sql = ''' INSERT INTO politician VALUES(3,'Alberto',1,'Curusego',null,'',1) '''
    conn.execute(sql)
    sql = ''' INSERT INTO politician VALUES(4,'Bufiobere',1,'Curusego',null,'',1) '''
    conn.execute(sql)
    sql = ''' INSERT INTO politician VALUES(5,'Flunodae',0,'',6,'Osceo',1) '''
    conn.execute(sql)
    sql = ''' INSERT INTO politician VALUES(6,'Osceo',5,'Flunodae',null,'',1) '''
    conn.execute(sql)
    sql = ''' INSERT INTO politician VALUES(7,'Envailslag',null,'',null,'',1) '''
    conn.execute(sql)
    return True


if __name__ == '__main__':
    #updateData()
    app.run(debug=True)
