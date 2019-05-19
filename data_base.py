import os
import random
import msvcrt
import time
import sys


os.system("mode con cols=150 lines=30")
clear = lambda: os.system('cls')

def lsort(lists, index): 
	"""Сортирует список по определенному индексу""" 
	if len(lists) <= 1:
		return lists
	else:
		q = random.choice(lists)
		s_nums = []
		m_nums = []
		e_nums = []
		for n in lists:
			if n[index] < q[index]:
				s_nums.append(n)
			elif n[index] > q[index]:
				m_nums.append(n)
			else:
				e_nums.append(n)
		return lsort(s_nums, index) + e_nums + lsort(m_nums, index)


def round(num, big=False):
	num = num / 1

	number = str(num).split('.')
	num = int(number[0])
	
	if big and number[1] != '0' and (number[0][0] != '-'):
			num += 1

	return num



class Table():
	"""Table - это класс, который представляет одну таблицу и все ее методы без графической оболочки.
		Возможно запрещенные методы: list.append(), 'str'.join(list), list.pop(), list.replace(), list.index(), list.extend(),
									 random.choise(), os.system(), isinstance(), raise, abs(), msvcrt.getch(), keyboard.read_key(), max(), split()

		Список методов:
		input_element - метод, позволяющий добавить или изменить информацию в таблице.
					 На вход принимает координаты изменяемой ячейки(x, y) и саму информацию.
					 Если координаты находятся вне таблицы, бросает исключение ValueError.
					 Если координаты переданы неправильного типа, бросает исключение TypeError
					 Функция ничего не озвращает

		delete_element - метод, позволяющий удалить информацию из таблицы. Принимает координаты изменяемой переменной.
						 Бросает те же ошибки, что и input_element. Ничего не возвращает

		search_element - метод, позволяющий найти совпадения переданного значения в таблице. 
						 Функция принимает элемент для поиска и список колонн в которых следует производить поиск. 
						 По умолчанию, функция ищет совпадения по всей таблице. Вернет исключение, если переданный столбец отсутствует в таблице
		sort_elemtnts - метод, позволяющий сортировать информацию по столбцам. Принимает индекс столбца, возвращает исключение, если такого нет. 
						"""




	def __init__(self, *args, table=None, **kwargs, ):

		if 'name' in kwargs:
			self.name = kwargs['name']

		if table != None:
			self.table = table
		else:
			self.width = len(args)
			self.table = [list(args), ['' for i in (self.width) * ' ']]  # создается cтруктура таблицы
			self.table[0].append("0")
			self.table[1].append("1")
		self.search_column = 0
		self.search_string = ''
		self.id_list = ['0', '1']
		self.cursor = [0, 0]

	def move_cursor(self, x, y):
		self.search_element()
		if self.cursor[0] + x < 0: self.cursor[0] = self.width - 1
		elif self.cursor[0] + x > self.width - 1: self.cursor[0] = 0
		elif self.cursor[1] + y < 0: self.cursor[1] = len(self.id_list) - 1
		elif self.cursor[1] + y > len(self.id_list) - 1: self.cursor[1] = 0
		else:
			self.cursor[0] += x
			self.cursor[1] += y
		

	def input_element(self, x, y, new_data): 
		"""
		   4. Проверка на то, что в конец таблицы добавился пустой список при добавлении элемента в конец
		   """
		new_data = str(new_data)
		if not isinstance(x, int) or not isinstance(y, int) or not isinstance(new_data, str):
			raise TypeError('x и y должны быть числом, new_data должна быть строкой')

		elif (abs(x + 1) > self.width) or (abs(y + 1) > len(self.table)): 
			raise ValueError('Такого элемента в таблице нет')

		elif y + 1 == len(self.table) and new_data.replace(' ','').replace('\n', '').replace('\t', '').replace('\v', '') != '':
			new_string = ['' for i in self.width * ' ']
			new_string.append(str(len(self.table)))
			self.table.append(new_string)
			self.table[y][x] = new_data		
		else:
			self.table[y][x] = new_data

	def delete_element(self, x, y):
		"""1. Проверка на то, что бросается ValueError при неккоректных координатах
		   2. Бросается исключение TypeError при передачи неккоректных данных
		   3. удаляется список, если он остается пустым
		   4. последний список не удаляется и остается пустым нисмотря ни на что
		"""
		self.input_element(x, y, '')

		if (''.join(self.table[y][:-1]) == '') and (y + 1 < len(self.table)):
			self.table.pop(y)
		for i in range(len(self.table)):
			self.table[i][-1] = str(i)


	def search_element(self):
		id_list = ['0']

		for i in range(len(self.table) - 1):
			if self.search_string in self.table[i + 1][self.search_column]:
				id_list.append(self.table[i + 1][-1])

		if str(len(self.table) - 1) not in id_list:
			id_list.append(str(len(self.table) - 1))
		self.id_list = id_list

	def sort_elements(self):
		new_table = [self.table[0]]
		new_table.extend(lsort(self.table[1:-1], self.cursor[0]))
		new_table.append(self.table[-1])
		self.table = new_table
		for i in range(len(self.table)):
			self.table[i][-1] = str(i)

		

	def print_table(self, max_string=25):
		max_x_list = []
		max_y_list = []
		string = ''
		table = self.table
		for i in range(self.width + 1):
			len_x = len(max(table, key=lambda x : len(x[i]))[i])

			if len_x > max_string:
				len_x = max_string
			max_x_list.append(len_x)

		for y in table:
			max_value = len(max(y, key=lambda y : len(y)))
			max_value = round(max_value / max_string, True)
			if max_value == 0:
				max_value = 1
			max_y_list.append(max_value)

		string += 'Поиск: ' + self.search_string + '\n'
		first_i = 0
		choise = False
		self.search_element()
		id_list = self.id_list
		for y, max_y,  in zip(table, max_y_list):
			if y[-1] in id_list:
				for i, max_x in enumerate(max_x_list):
					open_color = ''
					close_color = ''
					if (i == self.cursor[0] and first_i == self.cursor[1]) or (i == self.cursor[0] and first_i == self.cursor[1] + 1):
						open_color = '\x1b[31m'
						close_color = '\x1b[0m'
					if first_i == 0:
						if i == 0: simbol = '╔'
						else: simbol = '╦'
					else:
						if i == 0: simbol = '╠'
						else: simbol = '╬'
					string += simbol + open_color + '═' * (max_x + 2) + close_color


				if first_i == 0: string += '╗\n'
				else: string += '╣\n'

				y = list(y)
				for i in range(max_y):
					start , end = 0, max_string
					for x, max_x in enumerate(max_x_list):

						max_x -= len(y[x])
						if (x == self.cursor[0] and first_i == self.cursor[1]): 
							string += '\x1b[31m║ ' + (' ' * round(max_x / 2)) + y[x][start:end] + (' ' * round(max_x / 2, True)) + ' \x1b[0m'
						elif  (x == self.cursor[0] + 1 and first_i == self.cursor[1]):
							string += '\x1b[31m║\x1b[0m ' + (' ' * round(max_x / 2)) + y[x][start:end] + (' ' * round(max_x / 2, True)) + ' '
						else:
							string += '║ ' + (' ' * round(max_x / 2)) + y[x][start:end] + (' ' * round(max_x / 2, True)) + ' '

						y[x] = y[x][start + max_string:]
					start += max_string
					end += max_string

					if (self.width - 1 == self.cursor[0] and first_i == self.cursor[1]):
						string += '\x1b[31m║\x1b[0m\n'
					else:
						string += '║\n'
				first_i +=1

		for i, max_x in enumerate(max_x_list):
			simbol = '╩'
			if i == 0:
				simbol = '╚'
			if i == self.cursor[0] and len(self.table) - 1 == self.cursor[1]:
				string += simbol + '\x1b[31m═\x1b[0m' * (max_x + 2)
			else:
				string += simbol + '═' * (max_x + 2)

		string += '╝'

		# if first_i
		return string





class Interface():
	def __init__(self, **kwargs):
		self.help_table = Table('клавиша или сочетание', 'действие')
		self.menu = Table('Создать новую таблицу')
		self.menu.input_element(0, 1, "Загрузить существующую")
		self.help_table.input_element(0, 1, 'f1')
		self.help_table.input_element(0, 2, 'ctrl + s')
		self.help_table.input_element(0, 3, 'ctrl + fномер')
		self.help_table.input_element(0, 4, 'esc')
		self.help_table.input_element(0, 5, 'del')
		self.help_table.input_element(1, 1, 'помощь')
		self.help_table.input_element(1, 2, 'сохранить таблицу')
		self.help_table.input_element(1, 3, 'переход между таблицами')
		self.help_table.input_element(1, 4, 'выход')
		self.help_table.input_element(1, 5, 'удалить информацию в ячейке')
		
		self.tables = kwargs
		self.tables['help'] = self.help_table
		self.tables['menu'] = self.menu
		self.tables_list = list(self.tables.keys())
		self.cursor = 4


	def event_handler(self):

		key = msvcrt.getwch()
		choise_table = self.tables[self.tables_list[self.cursor]]
		if self.cursor == 4:
				choise_key = ''
				while choise_key != chr(13):
					clear()
					print('выберете ебучий пункт: ')
					print(choise_table.print_table())
					choise_key = msvcrt.getwch()
					if choise_key == u'\u00E0':
						choise_key = msvcrt.getwch()
						if ord(choise_key) == 75:
							choise_table.move_cursor(-1, 0)
							# print('вы нажали левую стрелочку')
						elif ord(choise_key) == 72:
							choise_table.move_cursor(0, -1)
							# print('вы нажали верхнюю стрелочку')
						elif ord(choise_key) == 77:
							choise_table.move_cursor(1, 0)
							# print('вы нажали правую стрелочку')
						elif ord(choise_key) == 80:
							choise_table.move_cursor(0, 1)
							# print('вы нажали нижнюю стрелочку')
						else:
							pass
					if key == chr(27):
						raise TypeError('Вы ебоклак. Esc на этом этапе делает выход из бд с помощью вызова ошибки')

				if choise_table.cursor[1] == 0:
					self.cursor = 0
				elif choise_table.cursor[1] == 1:
					self.cursor = 0
					table_num = 0
					with open('C:\\Users\\пользователь\\DataBase\\file.txt', encoding="UTF-8") as f:
						table = list()
				# 		for string in f:
				# 			if string == '\n':
				# 				self.tables[self.tables_list[table_num]].table = table
				# 				print(self.tables[self.tables_list[table_num]].table)
				# 				table.clear()
				# 				table_num += 1
				# 			else:
				# 				table.append(string.split(',')[:-1])




		elif key == u'\u0000':
			key = msvcrt.getwch()
			if ord(key) == 59:
				self.cursor = 3
				# print('вы нажали f1')
			elif ord(key) == 83:
				if choise_table.cursor[1] == 0:
					choise_table.search_string = ''
				else:
					choise_table.delete_element(choise_table.cursor[0], int(choise_table.id_list[choise_table.cursor[1]]))
				# print('вы нажали del')
			elif ord(key) == 94:
				self.cursor = 0
				# print('вы нажали ctrl+f1')
			elif ord(key) == 95:
				self.cursor = 1
				# print('вы нажали ctrl+f2')
			elif ord(key) == 96:
				self.cursor = 2
				# print('вы нажали ctrl+f3')
			else:pass
				# print('Произошла хуйня')
		elif key == u'\u00E0':
			key = msvcrt.getwch()
			if ord(key) == 75:
				choise_table.move_cursor(-1, 0)
				# print('вы нажали левую стрелочку')
			elif ord(key) == 72:
				choise_table.move_cursor(0, -1)
				# print('вы нажали верхнюю стрелочку')
			elif ord(key) == 77:
				choise_table.move_cursor(1, 0)
				# print('вы нажали правую стрелочку')
			elif ord(key) == 80:
				choise_table.move_cursor(0, 1)
				# print('вы нажали нижнюю стрелочку')
			else:
				# print('Произошла хуйня')
				pass

		elif key == chr(13):
			if int(choise_table.id_list[choise_table.cursor[1]]) == 0:
				choise_table.sort_elements()
			elif choise_table.cursor[0] == 0 and self.cursor == 0:
				table = self.tables[self.tables_list[1]]
				table.search_string = ''
				table.cursor = [0, 0]
				choise_key = ''
				while choise_key != chr(13):
					clear()
					print('выберете какую-нибудь хуету: ')
					print(table.print_table())
					choise_key = msvcrt.getwch()
					if choise_key == u'\u00E0':
						choise_key = msvcrt.getwch()
						if ord(choise_key) == 75:
							table.move_cursor(-1, 0)
							# print('вы нажали левую стрелочку')
						elif ord(choise_key) == 72:
							table.move_cursor(0, -1)
							# print('вы нажали верхнюю стрелочку')
						elif ord(choise_key) == 77:
							table.move_cursor(1, 0)
							# print('вы нажали правую стрелочку')
						elif ord(choise_key) == 80:
							table.move_cursor(0, 1)
							# print('вы нажали нижнюю стрелочку')
						else:
							pass
							# print('Произошла хуйня')
				ful_name = table.table[int(table.id_list[table.cursor[1]])][0]
				choise_table.input_element(choise_table.cursor[0], int(choise_table.id_list[choise_table.cursor[1]]), ful_name)

			elif choise_table.cursor[0] == 1 and self.cursor == 0:
				table = self.tables[self.tables_list[2]]
				table.search_string = ''
				table.cursor = [0, 0]
				choise_key = ''
				while choise_key != chr(13):
					clear()
					print('выберете какую-нибудь хуету: ')
					print(table.print_table())
					choise_key = msvcrt.getwch()
					if choise_key == u'\u00E0':
						choise_key = msvcrt.getwch()
						if ord(choise_key) == 75:
							table.move_cursor(-1, 0)
							# print('вы нажали левую стрелочку')
						elif ord(choise_key) == 72:
							table.move_cursor(0, -1)
							# print('вы нажали верхнюю стрелочку')
						elif ord(choise_key) == 77:
							table.move_cursor(1, 0)
							# print('вы нажали правую стрелочку')
						elif ord(choise_key) == 80:
							table.move_cursor(0, 1)
							# print('вы нажали нижнюю стрелочку')
						else:
							pass
							# print('Произошла хуйня')
				ful_name = table.table[int(table.id_list[table.cursor[1]])][0]
				choise_table.input_element(choise_table.cursor[0], int(choise_table.id_list[choise_table.cursor[1]]), ful_name)
					

			# print('вы нажали enter')

		elif key == chr(19):
			with open('C:\\Users\\пользователь\\DataBase\\file.txt', 'w', encoding='UTF-8') as f:
				for i in range(3):
					table = self.tables[self.tables_list[i]].table
					for string in table:
						for field in string:
							f.write(field + ',')
						f.write('\n')
					f.write('\n')
			print('\a')

			# print('вы нажали ctrl + s')

		elif key == chr(27):
			if self.cursor == 3:
				self.cursor = 0
			elif self.cursor in [0, 1, 2]:
				self.cursor = 4
			# print('вы  нажали esc')

		elif key == chr(8):
			if choise_table.cursor[1] == 0:
				choise_table.search_column = choise_table.cursor[0]
				choise_table.search_string = choise_table.search_string[:-1]
			else:
				field = choise_table.table[int(choise_table.id_list[choise_table.cursor[1]])][choise_table.cursor[0]]
				field = field[:len(field) - 1]
				choise_table.input_element(choise_table.cursor[0], int(choise_table.id_list[choise_table.cursor[1]]), field)
				# print("Вы нажали Backspace")
		else:
			if choise_table.cursor[1] == 0:
				choise_table.search_column = choise_table.cursor[0]
				choise_table.search_string += key
			else:
				# print('вы нажали ', ord(key))
				field = choise_table.table[int(choise_table.id_list[choise_table.cursor[1]])][choise_table.cursor[0]]
				field += key
				choise_table.input_element(choise_table.cursor[0], int(choise_table.id_list[choise_table.cursor[1]]), field)

if __name__ == "__main__":
	work_table = Table('Практическая работа', 'Студент', 'Вариант', 'Уровень задания', 'Дата сдачи', 'Оценка', name='таблица выполнения работ')
	practic_table = Table('Название работы', 'Количество часов', name='таблица практических работ')
	student_table = Table('ФИО', 'Оцека', name='таблица студентов') 
	
	interface = Interface(main=work_table, table0=practic_table, table1=student_table)


	while True:
		interface.event_handler()
		clear()
		print(interface.tables[interface.tables_list[interface.cursor]].print_table())
		
		

