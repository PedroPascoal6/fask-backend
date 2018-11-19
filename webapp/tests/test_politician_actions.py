from webapp.tests.utils import MyTest
from webapp.politician_actions import readDBPolitician, formatDataToFrontEnd,remove_subordinates_not_active
from webapp.models import generate_data


class TestPolitician(MyTest):
    def test_read_politicians(self):
        # Test if the relationship between subordinate and superior it's good
        politician_dictionary = readDBPolitician()
        print (politician_dictionary)
        for n in politician_dictionary:
            superior_id = politician_dictionary[n].get('attr').get('superiorid')
            # print("Actual ID : " + str(n) + " Superior ID : " + str(superior_id))
            if superior_id is not None and politician_dictionary[n] in politician_dictionary[superior_id].get(
                'children'):
                assert True
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


    def test(self):
        remove_subordinates_not_active(formatDataToFrontEnd(readDBPolitician())[0])
