from libs.app.schedule_config import ModelingSchedule
from libs.app.client_config import Modeling_Client
from colorama import Fore, Back, Style

class Context:
	"""
		Class used to control all the
		application context
	"""
	def __init__(self):
		self.schedule = ModelingSchedule()

	def __load_requirements(self):
		self.schedule.extract_db_entitys()
		self.schedule.extract_final_schedule()

	def __print_schedule(self) -> None:
		self.__load_requirements()
		print(10 * " - ", f" All Courts ", 10 * " - ", '\n')
		self.schedule.marked["court"] = self.schedule.see_schedule('court')
		print(10 * " - ", f" All Days ", 10 * " - ", '\n')
		print(Fore.YELLOW + f' => Court: {self.schedule.marked["court"]}')
		print(Style.RESET_ALL)
		self.schedule.marked["day"] = self.schedule.see_schedule(element='day', court=self.schedule.marked["court"])
		print(10 * " - ", f" All Times ", 10 * " - ", '\n')
		print(Fore.YELLOW + f' => Court: {self.schedule.marked["court"]} | Day: {self.schedule.marked["day"]}')
		print(Style.RESET_ALL)
		self.schedule.marked["time"] = self.schedule.see_schedule(element='time', court=self.schedule.marked["court"], day=self.schedule.marked["day"])

	def make_appointment(self) -> None:
		self.__print_schedule()
		if self.schedule.check_court_viability(self.schedule.marked):
			self.schedule.appointment.append((1,))
			self.schedule.post_appointment()
			print(Fore.YELLOW + f' => Court: {self.schedule.marked["court"]} | Day: {self.schedule.marked["day"]} | Time: {self.schedule.marked["time"]} - Reserved!')
			print(Style.RESET_ALL)
		else:
			print(Fore.RED + f' => Court: {self.schedule.marked["court"]} | Day: {self.schedule.marked["day"]} | Time: {self.schedule.marked["time"]} - NOT AVAILABLE!')
			print(Style.RESET_ALL)


	def cancel_appointment(self) -> None:
		self.__print_schedule()
		if not self.schedule.check_court_viability(self.schedule.marked):
			self.schedule.appointment.append((1,))
			self.schedule.delete_appointment()
			print(Fore.YELLOW + f' => Court: {self.schedule.marked["court"]} | Day: {self.schedule.marked["day"]} | Time: {self.schedule.marked["time"]} - Canceled!')
			print(Style.RESET_ALL)
		else:
			print(Fore.RED + f' => Court: {self.schedule.marked["court"]} | Day: {self.schedule.marked["day"]} | Time: {self.schedule.marked["time"]} - Not Reserved!')
			print(Style.RESET_ALL)

	def output_schedule_csv(self):
		print('Extracting schedule...')
		self.schedule.extract_final_schedule()
		self.schedule.output_appointments_csv()
		print('Extract Finished, and files created with success!')
