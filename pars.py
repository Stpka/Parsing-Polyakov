import requests
from bs4 import BeautifulSoup

questions = []
answers=[]
url = 'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=4&cat21=on&cat22=on&cat23=on'
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")


questions = soup.findAll('td', class_='topicview')
answers = soup.findAll('div', class_='hidedata')

def anqe(number):
	print(str(questions[number])[110:-23])
	print()
	print(str(answers[number])[80:-23])
	print('=============')
	print()

for number in range(5):
	anqe(number)