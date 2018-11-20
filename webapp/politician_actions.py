from datetime import datetime
from webapp.models import Politician, save_event, update_subordinates, resetSubordinates, set_politician_inactive

politician_dictionary = {}
data_formated = []


def readDBPolitician():
    # Read the politician from DB and construct the relationship between them from id's
    politician_dictionary.clear()
    politicians = Politician.query.all()
    print (politicians)
    for row in politicians:
        politician = {"attr": {"id": row.id,
                               "active": row.active,
                               "name": row.name,
                               "superiorid": row.superior_id,
                               "superiorid_original": row.superior_id_original,
                               "superiorName": row.superior_name,
                               "subordinateid": row.subordinate_id,
                               "subordinateName": row.subordinate_name,
                               "substitute_id": row.substitute_id,
                               "level": row.level
                               },
                      "children": []}

        politician_dictionary[row.id] = politician

    construct_sub_from_supID()
    return politician_dictionary


def construct_sub_from_supID():
    # Construct the subordinate's from superior ID
    for n in politician_dictionary:
        superior_id = politician_dictionary[n].get('attr').get('superiorid')
        if superior_id is not None:
            # Add all
            politician_dictionary[superior_id].get("children").append(politician_dictionary[n])
    return politician_dictionary


def formatDataToFrontEnd(politician_dictionary):
    # Formatar Data for frontend
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

def remove_subordinates_not_active(subordinate_list):
    #This delete the disable politicans from front-end Data
    print ("subordinate_list --->>" + str(subordinate_list))
    for subordinate in subordinate_list:
        # GET subordinates list
        if subordinate['attr'].get('children'):
            subordinate = {'attr': subordinate['attr'],
                              'children': remove_subordinates_not_active(
                                  subordinate['attr'].get('children'))}
        if not subordinate['attr'].get('active'):
            subordinate_list.remove(subordinate)
    return subordinate_list


def updatePoliticians():
    # Read from DB and format data to Front-End
    return formatDataToFrontEnd(readDBPolitician())


# def updatePoliticianOLD():
#     politicians = Politician.query.all()
#     data_formated = []
#     for row in politicians:
#         politician = {"attr": {"id": row.id,
#                                "active": row.active,
#                                "name": row.name,
#                                "superiorid": row.superior_id,
#                                "superiorName": row.superior_name,
#                                "subordinateid": row.subordinate_id,
#                                "subordinateName": row.subordinate_name},
#                       "children": []}
#
#         politician_dictionary[row.id] = politician
#
#     # Prencher os children
#     for n in politician_dictionary:
#         superior_id = politician_dictionary[n].get('attr').get('superiorid')
#         if superior_id is not None:
#             # Caso normal politico ativo
#             if politician_dictionary[n].get('attr').get('active'):
#                 politician_dictionary[superior_id].get("children").append(politician_dictionary[n])
#             # Caso em que o politico esta na jail, mas tem subordinados, o subordinado mais antigo é o da primeira posição
#             elif len(politician_dictionary[n].get('children')) != 0:
#                 politician_dictionary[superior_id].get("children").append(
#                     get_subordinate(politician_dictionary[n].get('children'), 0))
#                 # politician_dictionary[superior_id].get("children").append(politician_dictionary[n].get('children')[0])
#
#     for n in politician_dictionary:
#         superior_id = politician_dictionary[n].get("attr").get("superiorid")
#         is_active = politician_dictionary[n].get("attr").get("active")
#         if superior_id is None and is_active:
#             data_formated.append(politician_dictionary[n])
#         elif not politician_dictionary[superior_id].get("attr").get("active") and is_active:
#             data_formated.append(politician_dictionary[n])
#
#     return data_formated

def get_subordinate(childrens, politician_hash):
    if len(childrens) == 0:
        return None
    elif childrens[politician_hash].get('attr').get('active') is True:
        sup_politician = politician_dictionary[politician_hash]
        for subordinate_hash in sup_politician.get('children'):
            if sup_politician.get('children')[subordinate_hash].get("id") != childrens[politician_hash].get("id"):
                childrens[politician_hash].get("children").append(
                    politician_dictionary[politician_hash].get('children')[subordinate_hash])
        return childrens[politician_hash]
    else:
        get_subordinate(childrens[politician_hash + 1], politician_hash + 1)


def createEventOnJail(politician_id):
    readDBPolitician()
    superior_id = updateSubordinates_OnJail(politician_id)
    print ("substitute ID ---->" + str(superior_id))
    if superior_id != -1:
        set_politician_inactive(politician_id, superior_id)

    new_event_0 = {
        "date": datetime.now(),
        "politician_id": politician_id,
        "event_type": "1",
        "text": "IN",
    }
    save_event(new_event_0)


def updateSubordinates_OnJail_old(politician_id):
    # When politician go to Jail
    # 1 - All subordinates are immediately relocated to report to the oldest remaining superior at the same level as their previous one.
    # 2 - If there is no such possible alternative superior, the oldest direct subordinate of the previous superior is promoted to be the superior of the others.
    politician = politician_dictionary[int(politician_id)]
    superior_id = politician.get('attr').get('superiorid')
    if superior_id is not None and not politician_dictionary[int(superior_id)].get('attr').get('active'):
        updateSubordinates_OnJail(superior_id)
    elif superior_id is not None and politician_dictionary[int(superior_id)].get('attr').get('active'):
        update_subordinates(superior_id, politician_dictionary[int(politician_id)].get('children'), False)
        return superior_id
    elif superior_id is None and politician.get('attr').get('subordinateid') is not None:
        for politician_selected in politician.get('children'):
            if politician_selected.get('attr').get('active'):
                new_superior_id = politician_selected.get('attr').get('id')
                update_subordinates(new_superior_id, politician_dictionary[int(politician_id)].get('children'), True)
                return new_superior_id

def updateSubordinates_OnJail(politician_id):
    # When politician go to Jail find substitute
    # 1 - All subordinates are immediately relocated to report to the oldest remaining superior at the same level as their previous one.
    # 2 - If there is no such possible alternative superior, the oldest direct subordinate of the previous superior is promoted to be the superior of the others.
    if politician_id is None:
        return -1
    print("politician_id------>"+str(politician_id))
    politician = politician_dictionary[int(politician_id)]
    level = politician.get('attr').get('level')
    delegate_politician_list = Politician.query.filter_by(level=level).all()
    delegate_politician_id = -1
    for delegate_politician in delegate_politician_list:
        if delegate_politician is not None and delegate_politician.active and delegate_politician.id != int(politician_id):
            delegate_politician_id = delegate_politician.id
            return delegate_politician_id
            break
    if delegate_politician_id == -1:
        subordinate = politician_dictionary[int(politician.get('attr').get('subordinate_id'))]
        updateSubordinates_OnJail(Politician.query.filter_by(level=subordinate.get('attr').get('level')).first())




def createEventOffJail(politician_id):
    readDBPolitician()
    #substitute_id = politician_dictionary[int(politician_id)].get('attr').get('substitute_id')
    if politician_dictionary[int(politician_id)].get('attr').get('substitute_id') is None:
        return None
    else:
        substitute_id = politician_dictionary[int(politician_id)].get('attr').get('substitute_id')

    updateSubordinates_OutJail(politician_id, substitute_id)
    new_event_0 = {
        "date": datetime.now(),
        "politician_id": politician_id,
        "event_type": "1",
        "text": "OUT",
    }
    save_event(new_event_0)


def updateSubordinates_OutJail(politician_id, substitute_id):
    if substitute_id is not None:
        resetSubordinates(politician_id, politician_dictionary[substitute_id])
