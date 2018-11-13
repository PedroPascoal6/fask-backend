from flask import jsonify
from webapp.bdtools import updatePolitician,createEventOnJail,createEventOffJail



def dosomething():
    c = updatePolitician()
    return jsonify(c)


def to_array(rows):
    return [r._asdict() for r in rows]


def createEvent(politician_id, jail):
    if jail:
        createEventOnJail(politician_id)
    else:
        createEventOffJail(politician_id)