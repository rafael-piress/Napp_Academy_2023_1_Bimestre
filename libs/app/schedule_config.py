from libs.database.DB import DBStructure
from libs.app.model.client import Client
from colorama import init, Style, Fore


class Modeling_Schedule:
	"""
		Class that verify the schedule viability
		and return this information
	"""
	def __init__(self):
		self.db = DBStructure()
		self.filters = dict()
		self.schedule_day = list()
		self.schedule_time = list()
		self.court = list()
		self.occurrences_client = list()
		self.final_schedule = dict()

	def extract_db_entitys(self):
		if len(self.schedule_day) == 0:
			self.filters['sports_key_control_id'] = 1
			self.db.db_read('sports_value_control', self.filters)
			self.schedule_day = [result[2:] for result in self.db.results]
		if len(self.schedule_time) == 0:
			self.filters['sports_key_control_id'] = 2
			self.db.db_read('sports_value_control', self.filters)
			self.schedule_time = [result[2:] for result in self.db.results]
		if len(self.court) == 0:
			self.filters['sports_key_control_id'] = 3
			self.db.db_read('sports_value_control', self.filters)
			self.court = [result[2:] for result in self.db.results]
		self.db.db_read('sports_key_value_occurrences')
		self.occurrences_client = [result[3:] for result in self.db.results]
		self.occurrences = [result[3:-1] for result in self.db.results]

	def extract_final_schedule(self):
		if len(self.occurrences_client) > 0:
			for court in self.court:
				for day in self.schedule_day:
					for time in self.schedule_time:
						try:
							control = self.final_schedule[court[2]]
						except KeyError:
							self.final_schedule[court[2]] = dict()
						try:
							control = self.final_schedule[court[2]][day[2]]
						except KeyError:
							self.final_schedule[court[2]][day[2]] = dict()
						try:
							control = self.final_schedule[court[2]][day[2]][time[2]]
						except KeyError:
							self.final_schedule[court[2]][day[2]][time[2]] = bool()
						if (court[0], day[0], time[0]) in self.occurrences:
							self.final_schedule[court[2]][day[2]][time[2]] = False
						else:
							self.final_schedule[court[2]][day[2]][time[2]] = True
							self.final_schedule[court[2]]['availiable'] = True
							self.final_schedule[court[2]][day[2]]['availiable'] = True
					try:
						control = self.final_schedule[court[2]][day[2]]['availiable']
					except KeyError:
						self.final_schedule[court[2]][day[2]]['availiable'] = False
				try:
					control = self.final_schedule[court[2]]['availiable']
				except KeyError:
					self.final_schedule[court[2]]['availiable'] = False

		else:
			self.extract_db_entitys()
			if len(self.occurrences_client) > 0:
				self.extract_final_schedule()

	def check_court_viability(self, court: str, day: str or None = None, time: str or None = None):
		try:
			control = self.final_schedule[court]
		except KeyError:
			self.extract_final_schedule()
			self.check_court_viability(court)
		if day and time:
			return self.final_schedule[court][day][time]
		elif day:
			return self.final_schedule[court][day]
		else:
			return self.final_schedule[court] 

	def see_schedule(self, element: str, court: str or None = None, day: str or None = None, time: str or None = None):
		if len(self.final_schedule) > 0:
			if element == 'court':
				loop_element = self.final_schedule
			elif element == 'day':
				if court:
					loop_element = self.final_schedule[court]
			elif element == 'time':
				if day:
					loop_element = self.final_schedule[court][day]
			dict_control = dict()
			while True:
				init()
				for count, db_entity in enumerate(loop_element.keys()):
					space = (10 - len(db_entity)) * ' '
					if db_entity == 'availiable':
						continue
					elif element == 'time':
						if loop_element[db_entity]:
							space += '' if count >= 9 else ' '
							print(f'\t[{count + 1}] {element.capitalize()} - {db_entity}{space} | ' + Fore.GREEN + "AVAILIABLE")
							print(Style.RESET_ALL)
						else:
							space += '' if count >= 9 else ' '
							print(f'\t[{count + 1}] {element.capitalize()} - {db_entity}{space} | ' + Fore.RED + "NOT AVAILIABLE")
							print(Style.RESET_ALL)
					else:
						if loop_element[db_entity]['availiable']:
							space += '' if count >= 9 else ' '
							print(f'\t[{count + 1}] {element.capitalize()} - {db_entity}{space} | ' + Fore.GREEN + "AVAILIABLE")
							print(Style.RESET_ALL)
						else:
							space += '' if count >= 9 else ' '
							print(f'\t[{count + 1}] {element.capitalize()} - {db_entity}{space} | ' + Fore.RED + "NOT AVAILIABLE")
							print(Style.RESET_ALL)
					dict_control[count] = db_entity
				try:
					decicion = int(input(f'{element.capitalize()}: '))
				except TypeError:
					print('Wrong caracter, try again!')
					continue
				if decicion in range(1, 5):
					break
			return dict_control[decicion - 1]
		else:
			raise ValueError('The schedule was not created!')
