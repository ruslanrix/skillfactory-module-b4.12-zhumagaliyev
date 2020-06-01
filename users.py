# импортируем библиотеку sqlalchemy и некоторые функции из нее
# импортируем datetime
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"

# базовый класс моделей таблиц
Base = declarative_base()

class User(Base):
	"""
	Описание структуры таблицы user для хранения регистрационных данных пользователей
	"""
	__tablename__ = 'user'

	# идентификатор пользователя, первичный ключ
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	# имя пользователя
	first_name = sa.Column(sa.Text)
	# фамилия пользователя
	last_name = sa.Column(sa.Text)
	# пол пользователя
	gender = sa.Column(sa.Text)
	# e-mail пользователя
	email = sa.Column(sa.Text)
	# дата рождения пользователя
	birthdate = sa.Column(sa.Text)
	# рост пользователя
	height = sa.Column(sa.REAL)

def connect_db():
	"""
	Устанавливает соединение к базе данных
	"""
	# создаем соединение к базе данных
	engine = sa.create_engine(DB_PATH)	
	# создаем фабрику сессию
	session = sessionmaker(engine)
	# возвращаем сессию
	return session()

def validate(birthdate):
	"""
	Проверяет на правильность введения даты рождения
	"""
	try:
		datetime.strptime(birthdate, '%Y-%m-%d')
	except ValueError:
		raise ValueError("Вы ввели неправильный формат даты, должно быть yyyy-mm-dd")

def valid_email(email):
	"""
	Проверяет на валидность введенный e-mail
	"""
	if '@' in email and '.' in email.split('@')[1]:
		return True
	else:
		raise ValueError("Введен некорректный e-mail")

def request_data():
	"""
	Регистрация новых пользователей
	"""
	print("Привет! Я запишу твои данные")
	# запрашиваем у пользователя данные
	first_name = input("Введите свое имя: ")
	last_name = input("Введите свою фамилию: ")
	gender = input("Введите ваш пол. \n 1 - мужской (по умолчанию) \n 2 - женский \n")
	if gender == 2:
		gender = "Female"
	else:
		gender = "Male"	
	email = input("Введите ваш email: ")
	valid_email(email)
	birthdate = input("Введите дату вашего рождения в формате yyyy-mm-dd: ")
	validate(birthdate)
	height = input("Введите ваш рост в см: ")
	# создаем нового пользователя
	user = User(
		first_name=first_name,
		last_name=last_name,
		gender=gender,
		email=email,
		birthdate=birthdate,
		height=height
		)
	# возвращаем созданного пользователя
	return user