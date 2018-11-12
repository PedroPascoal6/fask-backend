import sqlite3

def getPolitician():
    con = sqlite3.connect("politiciansBD.db")
    data = {}
    for row in con.execute("select * from politician"):
        data[row[0]] = {"name": row[1],
                        "superiorid": row[2],
                        "superiorName": row[3],
                        "subordinateid": row[4],
                        "subordinateName": row[5]}
    return data