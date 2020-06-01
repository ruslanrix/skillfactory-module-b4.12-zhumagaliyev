import users, find_athlete
from users import connect_db, request_data
from find_athlete import find_similiar

session = connect_db()
mode = input("Выберите режим \n1 - ввести данные нового пользователя\n2 - ближайшего к пользователю атлета\n ")
if mode == "1":
	user = request_data()
	# добавляем нового пользователя в сессию
	session.add(user)
	session.commit()
	print("Спасибо, данные сохранены!")
elif mode == "2":
	name = input("Введите имя пользователя для поиска: ")
	find_similiar(name, session)
else:
	print("Неверно ввели режим. До свидания!")