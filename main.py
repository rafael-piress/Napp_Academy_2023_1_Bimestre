from libs.app.schedule_config import ModelingSchedule
from libs.app.client_config import Modeling_Client
from colorama import Fore, Back, Style

'''
	It's possible to rent in blocks of
		1 Hour
		  or
		3 Hour
'''


def main() -> None:
	print(10 * " - ", " Attenuare's courts ", 10 * " - ")
	while True:
		try:
			desicion = int(input('\n\t[1] - See schedule\nChoose: '))
		except (TypeError, ValueError):
			print('Wrong caracter, try again!')
			continue
		if desicion not in range(1, 2):
			print('Wrong choice, try again!')
			continue
		else:
			break
	if desicion == 1:
		config = ModelingSchedule()
		config.extract_db_entitys()
		config.extract_final_schedule()
		print(10 * " - ", f" All Courts ", 10 * " - ", '\n')
		config.marked["court"] = config.see_schedule('court')
		print(10 * " - ", f" All Days ", 10 * " - ", '\n')
		print(Fore.YELLOW + f' => Court: {config.marked["court"]}')
		print(Style.RESET_ALL)
		config.marked["day"] = config.see_schedule(element='day', court=config.marked["court"])
		print(10 * " - ", f" All Times ", 10 * " - ", '\n')
		print(Fore.YELLOW + f' => Court: {config.marked["court"]} | Day: {config.marked["day"]}')
		print(Style.RESET_ALL)
		config.marked["time"] = config.see_schedule(element='time', court=config.marked["court"], day=config.marked["day"])
		if config.check_court_viability(config.marked):
			config.appointment_post.append((1,))
			config.post_appointment()
			print(Fore.YELLOW + f' => Court: {config.marked["court"]} | Day: {config.marked["day"]} | Time: {config.marked["time"]} - Reserved!')


if __name__ == '__main__':
	main()
