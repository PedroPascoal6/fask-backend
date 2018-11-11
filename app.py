from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    data = [{"attr": {"id": "t1",
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
    return jsonify(data)

app.run(debug=True)