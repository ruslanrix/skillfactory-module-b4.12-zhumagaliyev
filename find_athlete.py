# импортируем библиотеку sqlalchemy и некоторые функции из нее
# импортируем пользовательский класс User
# импортируем datetime
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from users import User
from datetime import datetime

# базовый класс моделей таблиц
Base = declarative_base()

class Athletes(Base):
	"""
	Описывает структуру таблицы athelete
	"""
	__tablename__ = 'athelete'
	# идентификатор атлета, первичный ключ
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	# возраст атлета
	age = sa.Column(sa.Integer)
	# дата рождения атлета
	birthdate = sa.Column(sa.Text)
	# пол атлета
	gender = sa.Column(sa.Text)
	# рост атлета
	height = sa.Column(sa.REAL)
	# имя атлета
	name = sa.Column(sa.Text)
	# вес атлета
	weight = sa.Column(sa.Integer)
	# количество золотых медалей
	gold_medals = sa.Column(sa.Integer)
	# количество серебряных медалей
	silver_medals = sa.Column(sa.Integer)
	# количество бронзовых медалей
	bronze_medals = sa.Column(sa.Integer)
	# общее количество медалей
	total_medals = sa.Column(sa.Integer)
	# вид спорта
	sport = sa.Column(sa.Text)
	# страна
	country = sa.Column(sa.Text)		

def research(query, user_birthdate, list_athletes):
	"""
	составляем список словарей данных по атлетам, чей рост наиболее близок
	или совпадает с ростом пользователя
	также находим самого близкого по возрасту атлета
	первый параметр - объект запроса по имени пользователя
	второй параметр - дата рождения пользователя в формате datetime
	третий параметр - запрос с выводом всех атлетов
	"""
	delta_height = query.height
	delta_birthdate = 10000
	athletes_height = []
	for athlete in list_athletes:
			if athlete.height is not None:
				if delta_height >= abs(float(athlete.height) * 100 - query.height):
					delta_height = abs(float(athlete.height) * 100 - query.height)
					athletes_height.append(athlete.__dict__)
			if delta_birthdate > abs(datetime.strptime(athlete.birthdate, '%Y-%m-%d') - user_birthdate).days:
				delta_birthdate = abs(datetime.strptime(athlete.birthdate, '%Y-%m-%d') - user_birthdate).days
				athlete_birthdate = athlete.__dict__
	if delta_height > float(athletes_height[0]['height']) * 100 - query.height:
			athletes_height.pop(0)
	return athletes_height, athlete_birthdate

def find_similiar(name, session):
	"""
	1) сначала сохраняем количество пользователей по ввведеному имени
	2) если количество больше 1, то уже осуществляем фильтрацию и вывод на экран
	ближайшего по дате рождения к данному пользователю 
	и ближайшего по росту к данному пользователю
	3) если иное количество, то выводим ошибку.
	"""
	query = session.query(User).filter(User.first_name == name).count()
	if query >= 1:
		query = session.query(User).filter(User.first_name == name).first()		
		user_birthdate = datetime.strptime(query.birthdate, '%Y-%m-%d')	
		athletes_height, athlete_birthdate = research(query, user_birthdate, session.query(Athletes).all())		
		i = 0	
		while len(query.first_name) > i:
			# отфильтровываем по наиболее близкому совпадению в имени
			result = []			
			for athlete in athletes_height:
				if athlete['name'][i] == query.first_name[i]:
					result.append(athlete)
			if len(result) == 0:
				break
			athletes_height = result
			i += 1
		print("Атлет {} с самым ближайшим ростом {} к данному пользователю ({}, {}). Вид спорта: {}".format(athletes_height[0]['name'], athletes_height[0]['height'], query.first_name, query.height, athletes_height[0]['sport']))
		print("Атлет {} с ближайшей датой рождения {} к данному пользователю ({}, {}). Вид спорта: {}".format(athlete_birthdate['name'], athlete_birthdate['birthdate'], query.first_name, query.birthdate, athlete_birthdate['sport']))
	else:
		print("Ошибка. Такой пользователь не найден.")