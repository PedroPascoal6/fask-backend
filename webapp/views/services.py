from flask import jsonify
from webapp.bdtools import updatePoliticians,createEventOnJail,createEventOffJail



def dosomething():
    c = updatePoliticians()
    return jsonify(c)


def to_array(rows):
    return [r._asdict() for r in rows]


def createEvent(politician_id, jail):
    print("createEvent jail->" + str(jail))
    if jail:
        createEventOnJail(politician_id)
    else:
        createEventOffJail(politician_id)