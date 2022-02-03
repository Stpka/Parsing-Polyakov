import requests
from bs4 import BeautifulSoup
import re


tasks=[  [],
		 [[108,-23],
		 [12, "Оптимальный маршрут по весовой матрице"],
		 [13, "Сопоставление вершин графа и весовой матрицы"]],
		 
		 [],

		 [[110,-23],
		 [169, "Базы данных: поиск в электронной таблице"]],

		 [[109,-23],
         [21, "Сокращение двоичного кода"],
		 [22, "Выбор кода для одной буквы"],
		 [23, "Помехоустойчивые коды"],
		 [25, "Выбор кодов для нескольких букв"],
		 [166, "Декодирование. Условие Фано"]],

		 [[110,-23],
		 [27, "Автомат для работы с числами"],
		 [28, "Автомат с битами чётности"],
		 [144,"Автомат с инверсией битовой записи"]],

		 [],

		 [[110,-23],
		 [38, "Информационный объём изображений"],
		 [39, "Информационный объём звуковых данных"]],

		 [[110, -23],
		 [42, "Анализ списка слов заданной длины"],
		 [43, "Сколько слов можно составить при заданных ограничениях?"],
		 [145, "Сколько чисел можно составить при заданных ограничениях?"]]

		  ]
		  
questions = []
answers=[]



def find_thing(string):
	if re.search(r"№&nbsp;", string).end() > 0: # Если в задаче есть картинка, то мы ее парсим

		resStart  = re.search(r"№&nbsp;", string).end() # Берём начальные срезы для номера задачи
		resFinish = re.search(r" ' ", string).start()-1
		out = int(string[resStart:resFinish]) 			# Парсим номер зная срезы
		return out



def GenerateImg(number_of_task):
	url = f'https://kpolyakov.spb.ru/cms/images/{number_of_task}.gif'
	#print(url)
	get = requests.get(url)

	name_of_task = f"{number_of_task}.jpg"
	out = open(name_of_task, "wb")
	
	out.write(get.content)
	out.close()
	return name_of_task


def GenerateTasks(number_of_task, section):
	url = f"https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId={number_of_task}&cat{section}=on"
	print(url)
	return url


def setup():
	STATE = 1 # Нормальное состояние

	task = int(input("Какой номер вы хотите проработать?: "))
	left_slice=tasks[task][0][0]	# Генерируем срезы для этого номера
	right_slice=tasks[task][0][1]

	print(tasks[task])
	number_of_section = int(input("Введите номер раздела: "))

	if number_of_section == 169:	STATE = 0
	# Так как в этом разделе используются одна и таже каинка, то спрасим ее сразу здесь единажды

	page = requests.get(GenerateTasks(task,number_of_section)) 	# Создаём страницу
	
	soup = BeautifulSoup(page.text, "html.parser")				# Начинаем парсить
	questions = soup.findAll('td', class_='topicview')
	answers = soup.findAll('div', class_='hidedata')
	print(questions)



	for number in range(int(input("Сколько задач хотите сгенерировать?: "))):
		AnswerAndQuestion(questions, answers, number, left_slice, right_slice, STATE)


def AnswerAndQuestion(questions, answers, number, left_slice, right_slice, STATE):
	if STATE == 0 : 
		GenerateImg(4282)
		print(str(questions[number])[left_slice:right_slice])
		print()
		print(str(answers[number])[80:-23])
		print('=============')
		print()

	else:
		GenerateImg(find_thing(str(questions[number])))

		print(str(questions[number])[left_slice:right_slice])
		print()
		print(str(answers[number])[80:-23])
		print('=============')
		print()


setup()
