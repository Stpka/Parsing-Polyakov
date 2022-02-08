import requests
from bs4 import BeautifulSoup
import re
import os

tasks=[  [],

		 [[12, "Оптимальный маршрут по весовой матрице"],
		 [13, "Сопоставление вершин графа и весовой матрицы"]],
		 
		 [[8, "Сопоставление столбцов таблицы истинности и переменных"]],

		 [[169, "Базы данных: поиск в электронной таблице"]],

		 [[21, "Сокращение двоичного кода"],
		 [22, "Выбор кода для одной буквы"],
		 [23, "Помехоустойчивые коды"],
		 [25, "Выбор кодов для нескольких букв"],
		 [166, "Декодирование. Условие Фано"]],

# №5
		[[27, "Автомат для работы с числами"],
		 [28, "Автомат с битами чётности"],
		 [144,"Автомат с инверсией битовой записи"]],

		 [[37, "Количество повторений цикла. Значение переменной после завершения цикла"],
		 [91, "Количество повторений цикла. Что было на входе?"]],

		 [[38, "Информационный объём изображений"],
		 [39, "Информационный объём звуковых данных"]],

		 [[42, "Анализ списка слов заданной длины"],
		 [43, "Сколько слов можно составить при заданных ограничениях?"],
		 [145, "Сколько чисел можно составить при заданных ограничениях?"]],

		 [[146, "Минимум, максимум и среднее значение"],
		 [147, "Условные вычисления"]],

# №10
		[[148,"Поиск слова в текстовом документе"]],

		 [[52, "Вычисление объёма для хранения массива данных"],
		 [53,"Информационный объём для хранения автомобильных номеров"],
		 [54, "Информационный объём для хранения паролей (кодов) + доп. сведения"],
		 [149, "Информационный объём для хранения паролей (кодов)"]],

		 [[55, "Исполнитель Робот"],
		 [56, "Исполнитель Чертёжник"],
		 [57, "Исполнитель Редактор"],
		 [58, "Другие исполнители"]],

		 [[59, "Количество путей в графе между двумя вершинами"]],

		 [[60, "Позиционные системы счисления с любыми основаниями"],
		 [61, "Уравнения с данными в различных системах счисления"],
		 [62, "Анализ арифметических выражений в разных системах счисления"]],

# №15		
		[[67,"Множества и логика: задачи с отрезками"],
		 [68, "Множества и логика: задачи на множества чисел"],
		 [69, "Множества и логика: задачи с делителями"],
		 [70, "Множества и логика: задачи с битовыми логическими операциями"],
		 [123, "Множество и логика: анализ неравенств на плоскости"],
		 [167, "Множества и логика: смешанные задачи"]],

		 [],

		 [],

		 [],

		 [],

		 [],

		 [],

		 [],

		 [],

		 [],

		  ]
		  
questions = []
answers=[]


def find_file(string):
	if re.search(r'<a href="ege-dbase/', string) != None:
		resStart  = re.search(r"<a href=\"ege-dbase/", string).end()
		resFinish = re.search(r".xls</a>", string).start()-6
		out = str(string[resStart:resFinish]) 
		url = f"https://kpolyakov.spb.ru/cms/files/ege-dbase/{out}"
		get = requests.get(url)
		outt = open(out, "wb")
		outt.write(get.content)
		outt.close()
		os.replace(f"{out}", f"files/{out}")
		return 1
	else: print('Нет файла .xls')


def find_number_of_task(string):
	if re.search(r"<img src=", string) != None: # Если в задаче есть картинка, то мы ее парсим

		resStart  = re.search(r"№&nbsp;", string).end() # Берём начальные срезы для номера задачи
		resFinish = re.search(r" ' ", string).start()-1
		out = int(string[resStart:resFinish]) 			# Парсим номер зная срезы
		return out

	else: return False


def find_text(string):
	resStart  = re.search(r"changeImageFilePath", string).end()+2
	resFinish = re.search(r"</script>", string).start()-8
	out = string[resStart:resFinish] 
	print('\n\n')	
	return out


def find_answer(string):
	resStart  = re.search(r'changeImageFilePath', string).end()+2
	resFinish = re.search(r"</script>", string).start()-8
	out = string[resStart:resFinish]
	return out


def GenerateImg(number_of_task):
	if number_of_task == False: return
	
	url = f'https://kpolyakov.spb.ru/cms/images/{number_of_task}.gif'
	get = requests.get(url)
	name_of_task = f"{number_of_task}.gif"
	out = open(name_of_task, "wb")	
	out.write(get.content)
	out.close()

	os.replace(f"{name_of_task}", f"img/{name_of_task}")
	return name_of_task


def GenerateTasks(number_of_task, section):
	url = f"https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId={number_of_task}&cat{section}=on"
	print(url)
	return url


def setup():
	STATE = 1 # Нормальное состояние

	# Если папкк ещё не созданы
	if not os.path.isdir("files") and not os.path.isdir("img"):
		os.mkdir("files")
		os.mkdir("img")


	task = int(input("Какой номер вы хотите проработать?: "))
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
		AnswerAndQuestion(questions, answers, number, STATE)


def out(questions, answers, number):
	find_file(str(questions[number]))
	print(find_text(str(questions[number])))
	print()
	print(find_answer(str(answers[number])))
	print('=============')	
	print()



def AnswerAndQuestion(questions, answers, number, STATE):
	if STATE == 0 : 
		GenerateImg(4282)
		out(questions, answers, number)
	else:
		GenerateImg(find_number_of_task(str(questions[number])))
		out(questions, answers, number)


setup()
