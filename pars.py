import requests
from bs4 import BeautifulSoup
import requests


tasks=[  [],
		 [[108,-23, -156, -154],
		 [12, "Оптимальный маршрут по весовой матрице"],
		 [13, "Сопоставление вершин графа и весовой матрицы"]],
		 
		 [],

		 [[110,-23, 859, 863],
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
	task = int(input("Какой номер вы хотите проработать?: "))
	left_slice=tasks[task][0][0]	# Генерируем срезы для этого номера
	right_slice=tasks[task][0][1]

	print(tasks[task])
	number_of_section = int(input("Введите номер раздела: "))

	STATE = 0
	if number_of_section == 169:
		img_left = tasks[3][0][-2]	#Срезы для парсинга номера фото
		img_right = tasks[3][0][-1]

	elif number_of_section == 12:
		img_left = tasks[1][0][-2]	#Срезы для парсинга номера фото
		img_right = tasks[1][0][-1]

	else:
		img_right, img_left = 0,0

	page = requests.get(GenerateTasks(task,number_of_section)) 	# Создаём страницу
	
	soup = BeautifulSoup(page.text, "html.parser")				# Начинаем парсить
	questions = soup.findAll('td', class_='topicview')
	answers = soup.findAll('div', class_='hidedata')
	#print(questions)



	for number in range(int(input("Сколько задач хотите сгенерировать?: "))):
		AnswerAndQuestion(questions, answers, number, left_slice, right_slice, img_left, img_right)


def AnswerAndQuestion(questions, answers, number, left_slice, right_slice, img_left, img_right):
	if img_left != 0:
		#print(img_left, img_right)
		#print(str(questions[number])[img_left:img_right])
		number_of_task = int(str(questions[number])[img_left:img_right]) # Парсим номер задачи
		#sprint(number_of_task)
		GenerateImg(number_of_task)


	print(str(questions[number])[left_slice:right_slice])
	print()
	print(str(answers[number])[80:-23])
	print('=============')
	print()


setup()

