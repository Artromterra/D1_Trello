import requests

# key_inp = input('Введите ваш ключ Trello:')
# token_inp = input('Введите ваш токен Trello:')
# board_id_inp = input('Введите ваш board_id Trello из строки в браузере:')
auth_params = {
	'key': 'e5743bdcbe1ce3ff0102ee594ea74f5e',
	'token': 'f57c5af58cdf789ed9f67a6fda581311058810cb3b83a098c70a5ea8399f7ee5',
}
base_url = "https://api.trello.com/1/{}"
board_id = 'yZEJAvnP'
# читаем нашу таблицу
def read():
	column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
	for column in column_data:
		task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
		print(column['name'], "задач: {}".format(len(task_data)))
		if not task_data:
			print('\t' + 'Нет задач!')
			continue
		for task in task_data:
			print('\t' + task['name'])
		
# создаем новую задачу
def create():
	name = input('Введите имя задачи:\n')
	column_name = input('Введите название колонки:\n')
	column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
	for column in column_data:
		if column['name'] == column_name:
			requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
			break
# перемещаем задачу между колонками
def move():
	name = input('Введите имя задачи, котрую хотите переместить:\n')
	column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
	task_id = []
	col_with_task = []
	# формируем списки с номерами id и названиями колонок
	for column in column_data:
		column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
		for task in column_tasks:
			if task['name'] == name:
				task_id.append(task['id'])
				col_with_task.append(column['name'])
# проверяем есть ли задачи с одинаковыми именами
	if len(task_id) > 1:
		print('Задач с этим именем несколько:')
		for i in range(len(task_id)):
			print(f"{i + 1}: из колонки {col_with_task[i]}")
		target_task = int(input('Введите номер задачи, котрую надо переместить\n')) - 1
		task_move = task_id[target_task]
	else:
		task_move = task_id[0]
# перемещаем задачу с выбранным номером
	column_name = input('Введите название колонки, куда перемещаем задачу:\n')	
	for column in column_data:
		if column['name'] == column_name:
			requests.put(base_url.format('cards') + '/' + task_move + '/idList', data={'value': column['id'], **auth_params})
			
# создаем новую колонку
def create_list():
	name = input('Введите название колонки:\n')
	column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
	for column in column_data:
		requests.post(base_url.format('lists'), data={'name': name, 'idBoard':column['idBoard'],  **auth_params})
		break

def start_main():
	choice = input('Нажмите 1, если хотите увидеть список задач,'
					'\nнажмите 2, чтобы создать новую задачу'
					'\nнажмите 3, чтобы переместить задачу в новую колонку'
					'\nнажмите 4, чтобы добавить новую колонку\n')
	if choice == '1':
		read()
	elif choice == '2':
		create()
	elif choice == '3':
		move()
	elif choice == '4':
		create_list()

if __name__ == "__main__":
	start_main()
		