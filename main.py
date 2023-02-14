from libs.app.schedule_config import Modeling_Schedule
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
		config = Modeling_Schedule()
		config.extract_db_entitys()
		config.extract_final_schedule()
		print(10 * " - ", f" All Courts ", 10 * " - ", '\n')
		court = config.see_schedule('court')
		print(10 * " - ", f" All Days ", 10 * " - ", '\n')
		print(Fore.YELLOW + f' => Court: {court}')
		print(Style.RESET_ALL)
		day = config.see_schedule(element='day', court=court)
		print(10 * " - ", f" All Times ", 10 * " - ", '\n')
		print(Fore.YELLOW + f' => Court: {court} | Day: {day}')
		print(Style.RESET_ALL)
		time = config.see_schedule(element='time', court=court, day=day)


if __name__ == '__main__':
	main()
