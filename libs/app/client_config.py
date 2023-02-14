from libs.database.DB import DBStructure
from libs.app.model.client import Client
from colorama import init, Style, Fore

class Modeling_Client:
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
		self.client = [result[3:] for result in self.db.results]
		if len(self.client) > 0:
			self.client = client
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
			return self.client
		else:
			raise TypeError('Client already Exists!')
