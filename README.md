# Проект Voka, сайт для оказания услуг связанных со зрением

# Для корректной работы приложения необходимо установить эти библиотеки
pip install -r requirements.txt
# Для корректной работы приложения необходимо произвести заполнение базы данных 
python manage.py makemigrations
python manage.py migrate
# Запустить сервер
python manage.py runserver
# Создать супер пользователся в роли админа 
python manage.py createsuperuser