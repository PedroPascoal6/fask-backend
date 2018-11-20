from random import randint

from webapp.tests.utils import MyTest
from webapp.politician_actions import readDBPolitician, formatDataToFrontEnd, remove_subordinates_not_active, \
    createEventOnJail
from webapp.models import generate_data, resetSubordinates, Event


class TestPolitician(MyTest):
    def test_reset_subordinates(self):
        politician_dictionary = readDBPolitician()

        # Random Choise
        politician_id = randint(0, len(politician_dictionary))

        # print ("politician_id ----->" + str(politician_id))

        subordinate_list_original = politician_dictionary[politician_id].get("children")

        # Send Politician to Jail
        createEventOnJail(politician_id)

        # Get substitute ID
        politician_dictionary = readDBPolitician()
        substitute_id = politician_dictionary[politician_id].get("attr").get("substitute_id")

        # Test Function
        # print("substitute_id----> " + str(substitute_id))
        resetSubordinates(politician_id, politician_dictionary[substitute_id])

        # Refresh
        politician_dictionary = readDBPolitician()
        subordinate_list_final = politician_dictionary[politician_id].get("children")

        assert (set(subordinate_list_original).issubset(subordinate_list_final))

    def test_read_politicians(self):
        # Test if the relationship between subordinate and superior it's good
        politician_dictionary = readDBPolitician()
        for n in politician_dictionary:
            superior_id = politician_dictionary[n].get('attr').get('superiorid')
            # print("Actual ID : " + str(n) + " Superior ID : " + str(superior_id))
            if superior_id is not None and politician_dictionary[n] in politician_dictionary[superior_id].get(
                    'children'):
                assert True

    def test_createEventOnJail(self):
        # Test when politicians go to jail
        politician_dictionary = readDBPolitician()

        # Random Choise
        politician_id = randint(0, len(politician_dictionary))

        # Test Function
        createEventOnJail(politician_id)

        # Get event

        event = Event.query.filter_by(politician_id=politician_id).first()

        assert (event.politician_id == politician_id)






        #
        # def test_format_data_for_frontend(self):
        #     data_formated = formatDataToFrontEnd(readDBPolitician())[0]
        #     for politician in data_formated:
        #         #print (politician)
        #         assert(politician.get('attr'))
        #
        # def test_remove_subordinates_not_active(self):
        #     politician_dictionary = remove_subordinates_not_active(formatDataToFrontEnd(readDBPolitician())[0])
        #     for n in politician_dictionary:
        #         superior_id = politician_dictionary[n].get('attr').get('superiorid')
        #         print("Actual ID : " + str(n) + " Superior ID : " + str(superior_id))
        #         assert politician_dictionary[n].get('attr').active
        #
        #
