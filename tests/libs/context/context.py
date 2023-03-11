from libs.app.schedule_config import ModelingSchedule
from libs.app.client_config import ModelingClient
from colorama import init, Fore, Back, Style

class Context:
	"""
		Class used to control all the
		application context
	"""
	def __init__(self):
		self.schedule = ModelingSchedule()
		self.client_config = ModelingClient()

	def __load_requirements(self):
		init()
		self.client = self.client_config.get_client_information()
		self.schedule.extract_db_entitys()
		self.schedule.extract_final_schedule()

	def __see_client(self):
		try:
			print(Fore.BLUE + f' => Client: {self.client.name}')
			print(Style.RESET_ALL)
		except AttributeError:
			self.__load_requirements()
			self.__see_client()

	def __print_schedule(self) -> None:
		self.__load_requirements()
		self.__see_client()
		print(10 * " - ", f" All Courts ", 10 * " - ", '\n')
		self.schedule.marked["court"] = self.schedule.see_schedule('court')
		self.__see_client()
		print(10 * " - ", f" All Days ", 10 * " - ", '\n')
		print(Fore.YELLOW + f' => Court: {self.schedule.marked["court"]}')
		print(Style.RESET_ALL)
		self.schedule.marked["day"] = self.schedule.see_schedule(element='day', court=self.schedule.marked["court"])
		self.__see_client()
		print(10 * " - ", f" All Times ", 10 * " - ", '\n')
		print(Fore.YELLOW + f' => Court: {self.schedule.marked["court"]} | Day: {self.schedule.marked["day"]}')
		print(Style.RESET_ALL)
		while True:
			try:
				decision = int(input('Schedule just hour or three hours?\n\t[1] - One Hour - R$ 100,00\n\t[3] - Three Hour - R$ 250,00\nChoice: '))
			except TypeError:
				print('Wrong character, try again!')
				continue
			if decision != 1 and decision != 3:
				print('Invalid option! Try again!')
				continue
			else:
				break
		if decision == 1:
			self.schedule.marked["time"] = self.schedule.see_schedule(element='time', court=self.schedule.marked["court"], day=self.schedule.marked["day"])
		elif decision == 3:
			self.schedule.marked["time"] = self.schedule.see_schedule(element='time', court=self.schedule.marked["court"], day=self.schedule.marked["day"], multiple=True)
			print(self.schedule.marked['time'])

	def make_appointment(self) -> None:
		self.__print_schedule()
		available = self.schedule.check_court_viability(self.schedule.marked)
		if available == True:
			self.schedule.appointment.append((self.client.id,))
			print('Trying to post')
			self.schedule.post_appointment()
			if type(self.schedule.marked["time"]) == list:
				for time in self.schedule.marked["time"]:
					self.__see_client()
					print(Fore.YELLOW + f' => Court: {self.schedule.marked["court"]} | Day: {self.schedule.marked["day"]} | Time: {time} - Reserved!')
					print(Style.RESET_ALL)
			else:
				self.__see_client()
				print(Fore.YELLOW + f' => Court: {self.schedule.marked["court"]} | Day: {self.schedule.marked["day"]} | Time: {self.schedule.marked["time"]} - Reserved!')
				print(Style.RESET_ALL)
		else:
			if type(self.schedule.marked["time"]) == list:
				for time in available:
					self.__see_client()
					print(Fore.RED + f' => Court: {self.schedule.marked["court"]} | Day: {self.schedule.marked["day"]} | Time: {time} - Not Availiable!')
					print(Style.RESET_ALL)
			else:
				self.__see_client()
				print(Fore.RED + f' => Court: {self.schedule.marked["court"]} | Day: {self.schedule.marked["day"]} | Time: {self.schedule.marked["time"]} - Not Availiable!')
				print(Style.RESET_ALL)

	def cancel_appointment(self) -> None:
		self.__print_schedule()
		if not self.schedule.check_court_viability(self.schedule.marked):
			self.schedule.appointment.append((1,))
			self.schedule.delete_appointment()
			self.__see_client()
			print(Fore.YELLOW + f' => Court: {self.schedule.marked["court"]} | Day: {self.schedule.marked["day"]} | Time: {self.schedule.marked["time"]} - Canceled!')
			print(Style.RESET_ALL)
		else:
			self.__see_client()
			print(Fore.RED + f' => Court: {self.schedule.marked["court"]} | Day: {self.schedule.marked["day"]} | Time: {self.schedule.marked["time"]} - Not Reserved!')
			print(Style.RESET_ALL)

	def see_client_specific_schedule(self):
		self.__load_requirements()
		self.__see_client()
		self.schedule.get_specific_client_schedule(self.client)
		for occurrence in self.schedule.specific_client_occurrences:
			print(Fore.YELLOW + f' => Court: {occurrence[0]} | Day: {occurrence[1]}{(10 - len(occurrence[1])) * " "}| Time: {occurrence[2]} - Reserved!')
		print(Style.RESET_ALL)

	def see_client_specific_debit(self):
		self.__load_requirements()
		self.__see_client()
		value = self.client_config.get_client_debit(self.client)
		print(f'Total = {value}')

	def output_schedule_csv(self):
		print('Extracting schedule...')
		self.schedule.extract_final_schedule()
		self.schedule.output_appointments_csv()
		print('Extract Finished, and files created with success!')
