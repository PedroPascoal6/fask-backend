from datetime import datetime
from webapp.models import Politician, Event, save_politician, save_event, setPoliticianInactive , setPoliticianActive

politician_dictionary = {}
data_formated = []


def updatePolitician():
    politicians = Politician.query.all()
    data_formated = []
    for row in politicians:
        politician = {"attr": {"id": row.id,
                               "active": row.active,
                               "name": row.name,
                               "superiorid": row.superior_id,
                               "superiorName": row.superior_name,
                               "subordinateid": row.subordinate_id,
                               "subordinateName": row.subordinate_name},
                      "children": []}

        politician_dictionary[row.id] = politician

    for n in politician_dictionary:
        superior_id = politician_dictionary[n].get('attr').get('superiorid')
        if superior_id is not None:
            # Caso normal politico ativo
            if politician_dictionary[n].get('attr').get('active'):
                politician_dictionary[superior_id].get("children").append(politician_dictionary[n])
            # Caso em que o politico esta na jail, mas tem subordinados, o subordinado mais antigo é o da primeira posição
            elif len(politician_dictionary[n].get('children')) != 0:
                politician_dictionary[superior_id].get("children").append(
                    get_subordinate(politician_dictionary[n].get('children'), 0))
                # politician_dictionary[superior_id].get("children").append(politician_dictionary[n].get('children')[0])

    for n in politician_dictionary:
        superior_id = politician_dictionary[n].get("attr").get("superiorid")
        is_active = politician_dictionary[n].get("attr").get("active")
        if superior_id is None and is_active:
            data_formated.append(politician_dictionary[n])
        elif not politician_dictionary[superior_id].get("attr").get("active") and is_active:
            data_formated.append(politician_dictionary[n])

    return data_formated


def get_subordinate(childrens, n):
    if len(childrens) == 0:
        return None
    elif childrens[n].get('attr').get('active') is True:
        return childrens[n]
    else:
        get_subordinate(childrens[n + 1], n + 1)


def generateData():
    new_politician_0 = {"id": "0",
                        "name": "Wibeu",
                        "active": True,
                        "superior_id": None,
                        "superior_name": None,
                        "subordinate_id": "1",
                        "subordinate_name": "Curusego"
                        }
    save_politician(new_politician_0)
    new_politician_1 = {"id": "1",
                        "name": "Curusego",
                        "active": True,
                        "superior_id": "0",
                        "superior_name": "Wibeu",
                        "subordinate_id": "2",
                        "subordinate_name": "Nalvar"
                        }
    save_politician(new_politician_1)
    new_politician_2 = {"id": "2",
                        "name": "Nalvar",
                        "active": False,
                        "superior_id": "1",
                        "superior_name": "Curusego",
                        "subordinate_id": None,
                        "subordinate_name": None
                        }
    save_politician(new_politician_2)
    new_politician_3 = {"id": "3",
                        "name": "Alberto",
                        "active": True,
                        "superior_id": "1",
                        "superior_name": "Curusego",
                        "subordinate_id": None,
                        "subordinate_name": None
                        }
    save_politician(new_politician_3)
    new_politician_4 = {"id": "4",
                        "name": "Bufiobere",
                        "active": True,
                        "superior_id": "1",
                        "superior_name": "Curusego",
                        "subordinate_id": None,
                        "subordinate_name": None
                        }
    save_politician(new_politician_4)
    new_politician_5 = {"id": "5",
                        "name": "Flunodae",
                        "active": False,
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
                        "subordinate_id": None,
                        "subordinate_name": None
                        }
    save_politician(new_politician_6)
    new_politician_7 = {"id": "7",
                        "name": "Envailslag",
                        "active": True,
                        "superior_id": None,
                        "superior_name": None,
                        "subordinate_id": None,
                        "subordinate_name": None
                        }
    save_politician(new_politician_7)
    new_event_0 = {"id": "1",
                   "date": datetime.now(),
                   "politician_id": "0",
                   "event_type": "1",
                   "text": "IN",
                   }
    save_event(new_event_0)
    new_event_0 = {"id": "2",
                   "date": datetime.now(),
                   "politician_id": "1",
                   "event_type": "1",
                   "text": "IN",
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


def createEventOnJail(politician_id):
    setPoliticianInactive(politician_id)

    new_event_0 = {
                   "date": datetime.now(),
                   "politician_id": politician_id,
                   "event_type": "1",
                   "text": "IN",
                   }
    save_event(new_event_0)


def createEventOffJail(politician_id):
    setPoliticianActive(politician_id)

    new_event_0 = {
                   "date": datetime.now(),
                   "politician_id": politician_id,
                   "event_type": "1",
                   "text": "OUT",
                   }
    save_event(new_event_0)
