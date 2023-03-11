from libs.app.schedule_config import ModelingSchedule
from libs.app.client_config import ModelingClient
from libs.app.model.client import Client
from libs.storage.DB import DBStructure
import time
import pytest


class Test_client:

    def test_client_defined(self):
        self.first_client = Client(0, 'steven', '19998457525')
        with pytest.raises(TypeError) as error:
            self.second_client = Client(1, 'mary', 19998457525)
        assert str(error.value) == "object of type 'int' has no len()"
        assert isinstance(self.first_client, Client)
        self.second_client = Client(1, 'mary', '19998457525')
        assert isinstance(self.second_client, Client)

    def test_client_defined_02(self):
        self.first_client = Client(0, 'steven', '19998457525')
        self.second_client = Client(1, 'mary', '19998457525')
        with pytest.raises(TypeError) as error:
            self.third_client = Client(2, 'robin', '198545')
        assert str(error.value) == 'Enter a valid Number!'
        assert isinstance(self.first_client, Client)
        assert isinstance(self.second_client, Client)

    def test_client_defined_03(self):
        self.test_client_defined_02()
        assert isinstance(self.first_client.name, str)
        assert isinstance(self.first_client.id, int)
        assert isinstance(self.first_client.phone_number, str)
        assert isinstance(self.first_client.exists, bool)


class Test_ModelingClient(Test_client):

    def load_client(self):
        self.test_client_defined()
        self.client_config = ModelingClient()

    def test_load_modeling_object(self):
        self.load_client()
        self.client_config.check_client_viability(self.first_client)
        assert self.first_client.exists == False

    def test_client_cadastration(self):
        self.load_client()
        self.client_config.client_cadastration(self.first_client)
        self.client_config.check_client_viability(self.first_client)
        assert self.first_client.exists == True

    def test_client_cadastration_02(self):
        self.load_client()
        with pytest.raises(TypeError) as error:
            self.client_config.client_cadastration(self.first_client)
        assert str(error.value) == "Client already Exists!"
        self.client_config.check_client_viability(self.first_client)
        assert self.first_client.exists == False

    def test_client_delete(self):
        self.load_client()
        self.client_config.db.db_delete('client', {'key': 'phone_number', 'key_value': "'19998457525'"})
        self.client_config.check_client_viability(self.first_client)
        assert self.first_client.exists == False


class Test_ModelingSchedule(Test_ModelingClient):

    def load_schedule(self):
        self.schedule_config = ModelingSchedule()
        self.schedule_config.extract_db_entitys()


    def test_modeling_schedule_data_type(self):
        self.load_schedule()
        assert isinstance(self.schedule_config.db, DBStructure)
        assert isinstance(self.schedule_config.filters, dict)
        assert isinstance(self.schedule_config.schedule_day, list)
        assert isinstance(self.schedule_config.schedule_day[0], tuple)
        assert len(self.schedule_config.schedule_day) == 7

    def test_modeling_schedule_data_type_02(self):
        self.load_schedule()
        assert isinstance(self.schedule_config.schedule_time, list)
        assert isinstance(self.schedule_config.schedule_time[0], tuple)
        assert len(self.schedule_config.schedule_time) == 11

    def test_modeling_schedule_data_type_03(self):
        self.load_schedule()
        assert isinstance(self.schedule_config.court, list)
        assert isinstance(self.schedule_config.court[0], tuple)
        assert len(self.schedule_config.court) == 4

    def test_modeling_schedule_data_type_04(self):
        self.load_schedule()
        assert isinstance(self.schedule_config.occurrences_client, list)
        assert isinstance(self.schedule_config.final_schedule, dict)
        assert isinstance(self.schedule_config.marked, dict)

    def test_modeling_schedule_data_type_05(self):
        self.load_schedule()
        assert isinstance(self.schedule_config.appointment, list)
        assert isinstance(self.schedule_config.all_times, list)
        assert isinstance(self.schedule_config.specific_client_occurrences, list)

    def test_final_schedule(self):
        self.load_schedule()
        self.schedule_config.extract_final_schedule()
        assert len(self.schedule_config.final_schedule.keys()) == 4
        assert list(self.schedule_config.final_schedule.keys()) == ['1', '2', '3', '4']

    def test_final_schedule_02(self):
        confirmation = list()
        weekdays = ['Monday', 'availiable', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.test_final_schedule()
        assert list(self.schedule_config.final_schedule['1'].keys()) == weekdays
        base_list = list(self.schedule_config.final_schedule['1'].keys())
        for element in base_list:
            confirmation.append(element in weekdays)
        assert confirmation.count(True) == 8

    def test_final_schedule_03(self):
        confirmation = list()
        time = ['09hs - 10hs', 'availiable', '10hs - 11hs', '11hs - 12hs', '13hs - 14hs', '15hs - 16hs', '16hs - 17hs', '17hs - 18hs', '18hs - 19hs', '19hs - 20hs', '20hs - 21hs', '21hs - 22hs']
        self.test_final_schedule()
        assert len(self.schedule_config.final_schedule['1']['Monday'].keys()) == 12
        base_list = list(self.schedule_config.final_schedule['1']['Monday'].keys())
        for element in base_list:
            confirmation.append(element in time)
        assert confirmation.count(True) == 12


    def test_schedule_cadastration(self):
        self.test_final_schedule()
        self.marked = {
            'court': '4',
            'day': 'Sunday',
            'time': '21hs - 22hs'}
        self.schedule_config.extract_final_schedule()
        is_enable = self.schedule_config.check_court_viability(self.marked)
        if is_enable:
            self.test_client_cadastration()
            self.first_client = self.client_config.check_client_viability(self.first_client)
            if self.first_client.exists:
                self.schedule_config.marked = self.marked
                self.schedule_config.appointment.append((self.first_client.id,))
                self.schedule_config.post_appointment()
                time.sleep(2)
                debit = self.client_config.get_client_debit(self.first_client)
                assert debit == 100
                self.schedule_config.extract_final_schedule()
                is_enable = self.schedule_config.check_court_viability(self.marked)
                assert is_enable is True
                self.client_config.db.db_delete('client_values', {'key': 'client_id', 'key_value': self.first_client.id})
                self.schedule_config.db.db_delete('sports_key_value_occurrences', {'key': 'client_id', 'key_value': self.first_client.id})
                time.sleep(2)
                self.schedule_config.extract_final_schedule()
                is_enable = self.schedule_config.check_court_viability(self.marked)
                assert is_enable is True
                self.test_client_delete()
