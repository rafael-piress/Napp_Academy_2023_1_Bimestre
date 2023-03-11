from libs.storage.DB import DBStructure
from libs.app.model.client import Client
from colorama import init, Style, Fore

class ModelingClient:
    """
        Class used to do operations with the database
        with a relation 
    """
    def __init__(self):
        self.db = DBStructure()
        self.filters = dict()

    def check_client_viability(self, client: Client):
        self.filters['name'] = f"'{client.name}'"
        self.filters['phone_number'] = f"'{client.phone_number}'"
        self.db.db_read('client', self.filters)
        self.clients = [result[2:] for result in self.db.results]
        if len(self.clients) > 0:
            self.client = Client(self.clients[0][0], self.clients[0][1], self.clients[0][2])
            self.client.exists = True
            return self.client
        else:
            self.client = client
            self.client.exists = False
            return self.client

    def client_cadastration(self, client: Client) -> Client:
        self.check_client_viability(client)
        if not self.client.exists:
            self.db.db_create('client', {'name': client.name, 'phone_number': client.phone_number})
            self.client.exists = True
            return self.check_client_viability(client)
        else:
            raise TypeError('Client already Exists!')

    def get_client_information(self):
        self.name = None
        self.phone_number = None
        print('\nCliente Session..')
        while True:
            try:
                self.name = str(input("\nEnter the client name: ")).strip()
                break
            except (TypeError, ValueError):
                print('This is a invalid combination of caracter, try again!')
                continue
        if self.name:
            while True:
                try:
                    self.phone_number = str(input("\nEnter the client's phone number: ")).strip()
                    self.phone_number = self.phone_number.replace('(', '').replace(')', '').replace('-', '')
                    if self.phone_number.isdigit():
                        if len(self.phone_number) >= 11:
                            break
                except (TypeError, ValueError):
                    print('This is a invalid combination of caracter, try again!')
                    continue
        self.client = self.check_client_viability(Client(0, self.name, self.phone_number))
        if not self.client.exists:
            while True:
                try:
                    decision = str(input('\nThis client is not registrated, do you want to include him?\n\n[Y] or [N]\nChoice: ')).strip()
                except (TypeError, AttributeError):
                    print('This is a invalid combination of caracter, try again!')
                    continue
                if decision.lower() != 'n' and decision.lower() != 'y':
                    print('Wrong choice, try again!')
                    continue
                else:
                    break
            if decision.lower() == 'y':
                return self.client_cadastration(self.client)
            else:
                self.client = Client(0, self.name, self.phone_number)
                self.get_client_information()
        else:
            return self.client

    def get_client_debit(self, client: Client):
        self.filters = dict()
        self.filters['client_id'] = client.id
        self.db.db_read('client_values', self.filters)
        try:
            return self.db.results[0][-1]
        except:
            return 0

    def payment(self, client: Client):
        payment = self.get_client_debit(client)
        if payment == 0:
            print("There's no debits!")
            return
        options = {1: 'Debit', 2: 'Credit', 3: 'Cash'}
        while True:
            print('Amount left: ', payment)
            print('Options of payment: \n\t[1] - Debit\n\t[2] - Credit\n\t[3] - Cash')
            decision = int(input('Choice: '))
            if decision not in list(options.keys()):
                print('Wrong choice! Try again!')
                continue
            else:
                while True:
                    value = float(input(f'How much your gonna pay in {options[decision]}?\n\tAmount: '))
                    if value > float(payment):
                        print('The amount is bigger then the order total!')
                        continue
                    else:
                        payment = float(payment) - value
                        break
                if payment == 0:
                    self._paid = True
                    print('Payment completed!')
                    break
        self.db.db_delete('client_values', {'key': 'client_id', 'key_value': client.id})
