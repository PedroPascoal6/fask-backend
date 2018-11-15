
from datetime import datetime
from webapp.models import Politician, Event, save_politician, save_event, setPoliticianInactive, setPoliticianActive, \
    updateSubordinates, resetSubordinates

politician_dictionary = {}
data_formated = []


def readDBPolitician():
    # TODO
    # 1 - ler da BD os politicos
    # 2 - Preencher os seus children
    # 3 - Criar a data para o front-end (metodo á parte)
    politician_dictionary.clear()
    politicians = Politician.query.all()

    for row in politicians:
        politician = {"attr": {"id": row.id,
                               "active": row.active,
                               "name": row.name,
                               "superiorid": row.superior_id,
                               "superiorid_original": row.superior_id_original,
                               "superiorName": row.superior_name,
                               "subordinateid": row.subordinate_id,
                               "subordinateName": row.subordinate_name,
                               "substitute_id": row.substitute_id},
                      "children": []}

        politician_dictionary[row.id] = politician
    # Prencher os children
    for n in politician_dictionary:
        superior_id = politician_dictionary[n].get('attr').get('superiorid')
        if superior_id is not None:
            # Adiciona todos independentemente se está ativo ou não
            politician_dictionary[superior_id].get("children").append(politician_dictionary[n])


def formatDataToFrontEnd():
    data_formated = []
    for n in politician_dictionary:
        is_active = politician_dictionary[n].get("attr").get("active")
        on_top = politician_dictionary[n].get("attr").get("superiorid") is None
        if is_active and on_top:
            politician_dictionary[n] = {'attr': politician_dictionary[n].get('attr'),
                                        'children': remove_subordinates_not_active(
                                            politician_dictionary[n].get("children"))

                                        }
            data_formated.append(politician_dictionary[n])
    return data_formated


def remove_subordinates_not_active_old(subordinate_list):
    for subordinate in subordinate_list:
        print ("subordinate id " + str(subordinate.get('attr').get('id')) + " active? " + str(
            subordinate.get('attr').get('active')))

        if not subordinate.get('attr').get('active') and subordinate.get('attr').get('id') != None:
            subordinate_list.remove(subordinate)
            print("subordinate id " + str(subordinate.get('attr').get('id')) + " removido")
        if subordinate.get('children') and subordinate.get('attr').get('active'):
            subordinate_copy = subordinate
            subordinate_list.remove(subordinate)
            subordinate = {'attr': subordinate_copy,
                           'children': remove_subordinates_not_active(subordinate_copy.get('children'))}
            subordinate_list.append(subordinate)
    return subordinate_list


def remove_subordinates_not_active(subordinate_list):
    print ("subordinate_list->" + str(subordinate_list))
    for subordinate in list(subordinate_list):
        print(
            "subordinado [" + str(subordinate.get('attr').get('id')) + "] tem filhos? " + str(
                subordinate.get('children')))
        if subordinate.get('children'):
            subordinate = {'attr': subordinate.get('attr'),
                           'children': remove_subordinates_not_active(subordinate.get('children'))}
            print("subordinado [" + str(subordinate.get('attr').get('id')) + "] nova lista ->" + str(subordinate_list))
        print("subordinado [" + str(subordinate.get('attr').get('id')) + "] está activo? ->" + str(
            subordinate.get('attr').get('active')))
        if not subordinate.get('attr').get('active'):
            subordinate_list.remove(subordinate)
    return subordinate_list


def updatePoliticians():
    readDBPolitician()
    return formatDataToFrontEnd()


def updatePoliticianOLD():
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

    # Prencher os children
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


# TODO TESTAR O CASO DE GANHAR OS SUBORDINADOS DO SUP
def get_subordinate(childrens, n):
    if len(childrens) == 0:
        return None
    elif childrens[n].get('attr').get('active') is True:
        sup_politician = politician_dictionary[n]
        for c in sup_politician.get('children'):
            if sup_politician.get('children')[c].get("id") != childrens[n].get("id"):
                childrens[n].get("children").append(politician_dictionary[n].get('children')[c])
        return childrens[n]
    else:
        get_subordinate(childrens[n + 1], n + 1)





def generateData():
    new_politician_0 = {"id": 0,
                        "name": "Wibeu",
                        "active": True,
                        "superior_id": None,
                        "superior_id_original": None,
                        "superior_name": None,
                        "subordinate_id": 1,
                        "subordinate_name": "Curusego"
                        }
    save_politician(new_politician_0)
    new_politician_1 = {"id": 1,
                        "name": "Curusego",
                        "active": True,
                        "superior_id": 0,
                        "superior_id_original": 0,
                        "superior_name": "Wibeu",
                        "subordinate_id": 2,
                        "subordinate_name": "Nalvar"
                        }
    save_politician(new_politician_1)
    new_politician_2 = {"id": 2,
                        "name": "Nalvar",
                        "active": True,
                        "superior_id": 1,
                        "superior_id_original": 1,
                        "superior_name": "Curusego",
                        "subordinate_id": None,
                        "subordinate_name": None
                        }
    save_politician(new_politician_2)
    new_politician_3 = {"id": 3,
                        "name": "Alberto",
                        "active": True,
                        "superior_id": 1,
                        "superior_id_original": 1,
                        "superior_name": "Curusego",
                        "subordinate_id": None,
                        "subordinate_name": None
                        }
    save_politician(new_politician_3)
    new_politician_4 = {"id": 4,
                        "name": "Bufiobere",
                        "active": True,
                        "superior_id": 1,
                        "superior_id_original": 1,
                        "superior_name": "Curusego",
                        "subordinate_id": None,
                        "subordinate_name": None
                        }
    save_politician(new_politician_4)
    new_politician_5 = {"id": 5,
                        "name": "Flunodae",
                        "active": True,
                        "superior_id": 0,
                        "superior_id_original": 0,
                        "superior_name": "Wibeu",
                        "subordinate_id": 6,
                        "subordinate_name": "Osceo"
                        }
    save_politician(new_politician_5)
    new_politician_6 = {"id": 6,
                        "name": "Osceo",
                        "active": True,
                        "superior_id": 5,
                        "superior_id_original": 5,
                        "superior_name": "Flunodae",
                        "subordinate_id": None,
                        "subordinate_name": None
                        }
    save_politician(new_politician_6)
    new_politician_7 = {"id": 7,
                        "name": "Envailslag",
                        "active": True,
                        "superior_id": None,
                        "superior_id_original": None,
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


# TODO metodo para colocar um politico da cadeia deve repor os estados
def createEventOnJail(politician_id):
    readDBPolitician()
    superior_id = updateSubordinates_OnJail(politician_id)
    print ("on create Event on Jail...superior_id = " + str(superior_id))
    setPoliticianInactive(politician_id, superior_id)

    new_event_0 = {
        "date": datetime.now(),
        "politician_id": politician_id,
        "event_type": "1",
        "text": "IN",
    }
    save_event(new_event_0)


def updateSubordinates_OnJail(politician_id):
    print ("AQUI->" + str(politician_dictionary))
    politician = politician_dictionary[int(politician_id)]
    superior_id = politician.get('attr').get('superiorid')
    if superior_id is not None and not politician_dictionary[int(superior_id)].get('attr').get('active'):
        updateSubordinates_OnJail(superior_id)
    elif superior_id is not None and politician_dictionary[int(superior_id)].get('attr').get('active'):
        updateSubordinates(superior_id, politician_dictionary[int(politician_id)].get('children'), False)
        return superior_id
    elif superior_id is None and politician.get('attr').get('subordinateid') is not None:
        for politician_selected in politician.get('children'):
            if politician_selected.get('attr').get('active'):
                new_superior_id = politician_selected.get('attr').get('id')
                updateSubordinates(new_superior_id, politician_dictionary[int(politician_id)].get('children'), True)
                return new_superior_id


# TODO metodo para retirar um politico da cadeia deve repor os estados
def createEventOffJail(politician_id):
    readDBPolitician()
    substitute_id = politician_dictionary[int(politician_id)].get('attr').get('substitute_id')
    setPoliticianActive(politician_id, None)
    updateSubordinates_OutJail(politician_id, substitute_id)
    new_event_0 = {
        "date": datetime.now(),
        "politician_id": politician_id,
        "event_type": "1",
        "text": "OUT",
    }
    save_event(new_event_0)


def updateSubordinates_OutJail(politician_id, substitute_id):
    print ("substitute_id -> " + str(substitute_id))
    if substitute_id is not None:
        resetSubordinates(politician_id, politician_dictionary[substitute_id])
