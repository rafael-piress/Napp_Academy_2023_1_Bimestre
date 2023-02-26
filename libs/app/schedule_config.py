from libs.storage.DB import DBStructure
from libs.app.model.client import Client
from colorama import init, Style, Fore
import pandas as pd


class ModelingSchedule:
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
		self.marked = dict()
		self.appointment = list()

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
		self.occurrences_client = [result[2:] for result in self.db.results]
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

	def check_court_viability(self, marked: dict):
		try:
			control = self.final_schedule[marked['court']]
		except KeyError:
			self.extract_final_schedule()
			self.check_court_viability(court)
		try:
			return self.final_schedule[marked['court']][marked['day']][marked['time']]
		except KeyError:
			raise ValueError('The schedule was not uploaded!')

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
			range_final = len(loop_element.keys()) + 1
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
				if decicion in range(1, range_final):
					break
			return dict_control[decicion - 1]
		else:
			raise ValueError('The schedule was not created!')

	def __extract_object_key(self, element: str) -> tuple:
		if self.court and self.schedule_day and self.schedule_time:
			for key in self.court + self.schedule_day + self.schedule_time:
				if str(key[2]) == str(element):
					self.appointment.append(key)
					return
		else:
			raise ValueError('The schedule was not uploaded!')

	def __extract_occurrence_sport_id(self) -> int:
		if self.appointment:
			control = list()
			final_occurrence = list()
			final_occurrence.append([element[0] for element in self.appointment])
			for occurrence in self.occurrences_client:
				for element_ in final_occurrence[0]:
					if element_ in occurrence:
						control.append(True)
				if len(control) == 4:
					return occurrence[0]
				else:
					control = list()

	def post_appointment(self):
		if self.marked and self.appointment:
			for element in self.marked.keys():
				self.__extract_object_key(self.marked[element])
		if len(self.appointment) == 4:
			sended_post = dict()
			for element in self.appointment:
				try:
					if element[1] == 1:
						sended_post['weekday_id'] = element[0]
					elif element[1] == 2:
						sended_post['schedule_id'] = element[0]
					elif element[1] == 3:
						sended_post['court_id'] = element[0]
				except IndexError:
					sended_post['client_id'] = element[0]
			if len(sended_post.keys()) == 4:
				self.db.db_create('sports_key_value_occurrences', sended_post)
				
		else:
			raise ValueError('The client schedule was not uploaded!')


	def delete_appointment(self):
		if self.marked and self.appointment:
			for element in self.marked.keys():
				self.__extract_object_key(self.marked[element])
		if len(self.appointment) == 4:
			sended_post = dict()
			delete_id = self.__extract_occurrence_sport_id()
			if delete_id:
				self.db.db_delete('sports_key_value_occurrences', {'key': 'occurrences_id', 'key_value': delete_id})
		else:
			raise ValueError('The client schedule was not uploaded!')

	def output_appointments_csv(self):
		output_elements = dict()
		if len(self.final_schedule.keys()) == 0:
			raise ValueError('The schedule was not uploaded!')
		output_elements.update(self.final_schedule)
		for court in output_elements.keys():
			for day in output_elements[court].keys():
				if type(output_elements[court][day]) is bool:
					if output_elements[court][day]:
						output_elements[court][day] = ''
					else:
						output_elements[court][day] = 'X'
				else:
					for schedule in output_elements[court][day].keys():
						if output_elements[court][day][schedule]:
							output_elements[court][day][schedule] = ''
						else:
							output_elements[court][day][schedule] = 'X'
		for court in output_elements.keys():
			frame_information = pd.DataFrame(output_elements[court])
			frame_information.to_csv(f'schedule_court_{court}.csv')
