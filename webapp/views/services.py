import json

from flask import jsonify
from flask_restful.representations import json
from sqlalchemy.ext.declarative import DeclarativeMeta
from webapp.bdtools import updatePolitician


def dosomething():
    c = updatePolitician()
    print (c)
    #return {}

    #return json.dumps([dict(r) for r in c])

    # data = bdtools.getData()
    return jsonify(c)


def to_array(rows):
    return [r._asdict() for r in rows]