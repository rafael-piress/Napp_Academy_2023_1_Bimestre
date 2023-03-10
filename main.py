from libs.context.context import Context

'''
	It's possible to rent in blocks of
		1 Hour
		  or
		3 Hour
'''


def main() -> None:
	print(10 * " - ", " Attenuare's courts ", 10 * " - ")
	desicion = 0
	while desicion != 10:
		while True:
			try:
				desicion = int(input(
				'\n\t[1] - Make a Appointment\n\t' +
				'[2] - Cancel a Appointment\n\t' +
				'[3] - See specific Client schedule\n\t' +
				"[4] - See specific Client's Debit\n\t" +
				'[9] - Extract schedule to csv\n\t' +
				'[10] - Exit\n' +
				'Choose: '))
			except (TypeError, ValueError):
				print('Wrong caracter, try again!')
				continue
			if desicion not in range(1, 11):
				print('Wrong choice, try again!')
				continue
			else:
				break
		context = Context()
		if desicion == 1:
			context.make_appointment()
		if desicion == 2:
			context.cancel_appointment()
		if desicion == 3:
			context.see_client_specific_schedule()
		if desicion == 4:
			context.see_client_specific_debit()
		if desicion == 9:
			context.output_schedule_csv()


if __name__ == '__main__':
	main()
