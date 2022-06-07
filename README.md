# KanbanTP

---

## О проекте

Вебсайт, сделанный с помощью фреймворка Django, реализуют систему канбан-доски.
Главный принцип канбан - это визуализация. Основная идея - сделат визуальую доску,
которую вы разобьете по необходимым для вас этапам и расположите задачу по её стадии развития.

![](https://skr.sh/sEKAQYHSJ14?a)

---

## Установка

Клонируем проект в выбранную директорию.

````
git clone https://github.com/Nishtyachok/KanbanTP.git
````

Настраиваем виртуальную среду.

````
cd KanbanTP
python -m venv venv
cd venv/Scripts
activate.bat
````

Для установки нужных библиотек, в главной директории проекта прописываем команду

````
pip install -r requierments.txt 
````

Теперь наш проект готов к использоанию.

---

## Использование

Находясь в корневой директории проекта, прописываем в командную строку

````
cd mysite
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
````

Далее в браузере переходим по ссылке http://127.0.0.1:8000/.

---
И видим что все у нас работает
![Screenshot_1](https://user-images.githubusercontent.com/51389727/172386152-7089b3bd-b2bd-4898-b1ae-af39bb839eb3.png)
