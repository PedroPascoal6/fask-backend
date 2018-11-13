import sqlite3
from datetime import datetime
from webapp.models import Politician, Event, save_politician, save_event

data = {}


def updatePolitician():
    politicians = Politician.query.all()

    for row in politicians:
        data[row.id] = {"name": row.name,
                               "superiorid": row.superior_id,
                               "superiorName": row.superior_name,
                               "subordinateid": row.subordinate_id,
                               "subordinateName": row.subordinate_name}


        # subordinates, politicians = {}
        # for row in con.execute("select * from politician"):
        #     politicians[row[0]] = {"name": row[1],
        #                            "superiorid": row[2],
        #                            "superiorName": row[3],
        #                            "subordinateid": row[4],
        #                            "subordinateName": row[5]}
        #
        # for row in con.execute("select * from politicianEvent"):
        #     if row[3] == 1:
        #         subordinates[row[2]] = {"subordinates": row[4].split(";")[0].split("=") + data[row[2]].get("subordinates")}
        # data = {subordinates, politicians}
    return data


def getData():
    return data


def generateData():
    new_politician_0 = {"id": "0",
                        "name": "Wibeu",
                        "active": True,
                        "superior_id": "null",
                        "superior_name": "",
                        "subordinate_id": "1",
                        "subordinate_name": "Curusego"
                        }
    save_politician(new_politician_0)
    new_politician_1 = {"id": "1",
                        "name": "Curusego",
                        "active": True,
                        "superior_id": "1",
                        "superior_name": "Curusego",
                        "subordinate_id": "2",
                        "subordinate_name": "Nalvar"
                        }
    save_politician(new_politician_1)
    new_politician_2 = {"id": "2",
                        "name": "Nalvar",
                        "active": True,
                        "superior_id": "1",
                        "superior_name": "Curusego",
                        "subordinate_id": "",
                        "subordinate_name": ""
                        }
    save_politician(new_politician_2)
    new_politician_3 = {"id": "3",
                        "name": "Alberto",
                        "active": True,
                        "superior_id": "1",
                        "superior_name": "Curusego",
                        "subordinate_id": "",
                        "subordinate_name": ""
                        }
    save_politician(new_politician_3)
    new_politician_4 = {"id": "4",
                        "name": "Bufiobere",
                        "active": True,
                        "superior_id": "1",
                        "superior_name": "Curusego",
                        "subordinate_id": "",
                        "subordinate_name": ""
                        }
    save_politician(new_politician_4)
    new_politician_5 = {"id": "5",
                        "name": "Flunodae",
                        "active": True,
                        "superior_id": "0",
                        "superior_name": "Wibeu",
                        "subordinate_id": "6",
                        "subordinate_name": "Osceo"
                        }
    save_politician(new_politician_5)
    new_politician_6 = {"id": "6",
                        "name": "Osceo",
                        "active": True,
                        "superior_id": "5",
                        "superior_name": "Flunodae",
                        "subordinate_id": "",
                        "subordinate_name": ""
                        }
    save_politician(new_politician_6)
    new_politician_7 = {"id": "7",
                        "name": "Envailslag",
                        "active": True,
                        "superior_id": "",
                        "superior_name": "",
                        "subordinate_id": "",
                        "subordinate_name": ""
                        }
    save_politician(new_politician_7)
    new_event_0 = {"id": "0",
                   "date": datetime.now(),
                   "politician_id": "0",
                   "event_type": "1",
                   "text": "added=1",
                   }
    save_event(new_event_0)
    # con.execute(sql)
    # sql = ''' INSERT INTO politicianEvent VALUES(1,'''+str(datetime.now())+''',0,'1',"added=2") '''
    # con.execute(sql)
    # sql = ''' INSERT INTO politicianEvent VALUES(2,'''+str(datetime.now())+''',0,'1',"added=3") '''
    # con.execute(sql)
    # sql = ''' INSERT INTO politicianEvent VALUES(3,'''+str(datetime.now())+''',0,'1',"added=4") '''
    # con.execute(sql)
    # sql = ''' INSERT INTO politicianEvent VALUES(4,'''+str(datetime.now())+''',1,'1',"added=5") '''
    # con.execute(sql)
    # sql = ''' INSERT INTO politicianEvent VALUES(5,'''+str(datetime.now())+''',1,'1',"added=6") '''
    # con.execute(sql)
