#  SQL, Models and Migrations

## Data types in SQLite

- `TEXT`: текстові рядки (наприклад, ім’я людини);
- `NUMERIC`: загальна форма числових даних (наприклад, дата чи булевий вираз);
- `INTEGER`: будь-яке ціле число (наприклад, вік людини);
- `REAL`: будь-яке дійсне число (наприклад, вага людини);
- `BLOB`: двійковий великий об’єкт (наприклад, зображення).

## Tables
- Команда створення таблиці [CREATE TABLE](https://www.w3schools.com/sql/sql_create_table.asp)  
- Можливі [оператори обмеження](https://www.tutorialspoint.com/sqlite/sqlite_constraints.htm) при створенні таблиці, наприклад `NOT NULL` або `PRIMARY KEY`  
```sql
CREATE TABLE flights(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    duration INTEGER NOT NULL
);
```
- Команда додавання даних до таблиці [INSERT](https://www.tutorialspoint.com/sqlite/sqlite_insert_query.htm):

```sql
INSERT INTO flights
    (origin, destination, duration)
    VALUES ("New York", "London", 415);
```

- Команда вибору даних з таблиці [SELCT](https://www.tutorialspoint.com/sqlite/sqlite_select_query.htm):  
```sql
SELECT * FROM flights;
SELECT origin, destination FROM flights;
SELECT * FROM flights WHERE id = 3;
SELECT * FROM flights WHERE origin = "New York";
SELECT * FROM flights WHERE duration > 500;
SELECT * FROM flights WHERE duration > 500 AND destination = "Paris";
SELECT * FROM flights WHERE origin IN ("New York", "Lima");
SELECT * FROM flights WHERE origin LIKE "%a%";
```

## Working with SQL in the terminal

1. Підготовка до роботи:  
- Встановлюємо [SQLite](https://www.sqlite.org/download.html)  
- Встановлюємо [браузер БД](https://sqlitebrowser.org/dl/)
2. Робота в командному рядку:  
- Створимо файл бази даних у терміналі:  
`touch flaights.sql`  
- Відкриваємо створений файл у СУБД:  
`C:\sqlite\sqlite3 flaights.sql`
3. Створюємо нову таблицю в БД:  
```sql
CREATE TABLE flights(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    duration INTEGER NOT NULL
);
```
- перевіряємо:  
`.tables`  

4. Додамо дані в щойно створену таблицю:
```sql
INSERT INTO flights (origin, destination, duration) VALUES ("New York", "London", 415);
INSERT INTO flights (origin, destination, duration) VALUES ("Shanghai", "Paris", 760);
INSERT INTO flights (origin, destination, duration) VALUES ("Istanbul", "Tokyo", 700);
INSERT INTO flights (origin, destination, duration) VALUES ("New York", "Paris", 435);
INSERT INTO flights (origin, destination, duration) VALUES ("Moscow", "Paris", 245);
INSERT INTO flights (origin, destination, duration) VALUES ("Lima", "New York", 455);
```
- перевіряємо:
```sql
SELECT * FROM flights;
```
- покращуємо моделювання колонок та додаємо заголовки для команди `SELECT`:  
`.mode columns`  
`.headers yes`  

5. Роблячи вибірку даних також можливо використовувати функції такі як [AVERAGE, COUNT, MAX, MIN, SUM](https://www.w3schools.com/sql/sql_count_avg_sum.asp)

## Changing the data in the table

1. Оператор 'UPDATE'  
```sql 
UPDATE flights SET duration = 430 WHERE origin = "New York" AND destination = "London";
```
2. Оператор видалення даних за певних умов `DELETE`  
```sql
DELETE FROM flights WHERE destination = "Tokyo";
```
3. Інші умови вибірки даних:  
- [LIMIT](https://www.w3schools.com/sql/sql_top.asp): обмежує кількість результатів, повернутих за запитом;
- [ORDER BY](https://www.w3schools.com/sql/sql_orderby.asp): впорядковує результати на основі вказаної колонки;
- [GROUP BY](https://www.w3schools.com/sql/sql_groupby.asp): групує результати за вказаною колонкою;
- [HAVING](https://www.w3schools.com/sql/sql_having.asp): дає змогу встановлювати додаткові обмеження за кількістю результатів.

## Joining tables JOIN request

1. Приклад синтаксису простого запиту INNER JOIN (що означає ігнорування рядків, які не мають збігів між таблицями):  
```sql
SELECT first, origin, destination
FROM flights JOIN passengers
ON passengers.flight_id = flights.id;
``` 
2. По інших видах запитів об'єднання таблиць дивіться документацію за посиланням:

- [LEFT JOIN](https://www.w3schools.com/sql/sql_join_left.asp): повертає всі рядки лівої таблиці, та тільки ті що відповідають умові з правої
- [RIGHT JOIN](https://www.w3schools.com/sql/sql_join_right.asp): протилежно попередньому запиту
- [FULL OUTER JOIN](https://www.w3schools.com/sql/sql_join_full.asp): повертає усі рядки з лівої або правої таблиць якщо вони відповідають умові

## Django models

1. `: моделі Django` — це рівень абстракції поверх SQL, що дає нам змогу працювати з базами даних, використовуючи класи та об’єкти Python, а не прямі SQL-запити.
2. Почнімо використовувати моделі, створивши джанго-проект для нашої авіакомпанії та створивши застосунок у цьому проекті.
```python  
django-admin startproject airline
cd airline
python manage.py startapp flights
```
3. Додамо `flights` до списку `INSTALLED_APPS` у `settings.py`   

4. Додамо маршрут для `flights` в `urls.py`:  
`path("flights/", include("flights.urls")),`  

5. Створіть файл `urls.py` у застосунку `flights`. І заповніть його стандартними імпортами та списками urls.py:  
```python
from django.urls import path
from . import views
urlpatterns = []
```
6. Замість створення власне шляхів і початку роботи з `views.py`, ми створимо моделі у файлі `models.py`, та опишемо які дані хочемо зберігати в нашому застосунку.  
Потім Django визначить синтаксис SQL, необхідний для зберігання інформації про кожну з наших моделей. Фактично кожна модель відповідає таблиці в якій ми будемо зберігати інформацію. Приклад таблиці (моделі) для одного рейсу:
```python
class Flight(models.Model):                         # створюємо модель, що наслідує клас моделей Django
    origin = models.CharField(max_length=64)        # поле таблиці/моделі, що відповідає пункту вильоту довжиною до 64 символів
    destination = models.CharField(max_length=64)  
    duration = models.IntegerField()
```
Про інші вбудовані типи даних полів можна прочитати [тут](https://docs.djangoproject.com/en/3.0/ref/forms/fields/#built-in-field-classes)   

## Migrations (Міграції)  

1. Не дивлячись на те, що ми створили модель у файлі `models.py`, якщо ми подивимось в каталог, то побачимо, що у нас досі немає бази даних для зберігання цієї інформації:  

![sql](.img/migrate1.jpg)  

2. Переходимо до основного каталогу нашого проекту та створюємо базу даних із наших моделей:  

`python manage.py makemigrations`  

3. Ця команда генерує певні файли Python, які створять або змінять нашу базу даних, щоб мати можливість зберігати те, що маємо в наших моделях:  

![sql](.img/makemigration.jpg)  

4. Щоб застосувати ці міграції до нашої бази даних, виконаємо команду:  

`python manage.py migrate`

5. Тепер ви побачите, що у каталозі нашого проекту з’явився файл `db.sqlite3`.

## Shell
1. Щоб взаємодіяти з базою даних та тестувати запити можемо скористатися оболонкою, де зможемо виконувати команди Python у межах нашого проекту:  

`python manage.py shell`   
2. Далі виконуємо наступні команди для отримання досвіду роботи з shell:  
```python 
# Імпортувати модель flights
In [1]: from flights.models import Flight

# Створити новий рейс
In [2]: f = Flight(origin="New York", destination="London", duration=415)

# Вставити цей рейс до нашої бази даних
In [3]: f.save()

# Зробити запит до всіх рейсів в базі даних
In [4]: Flight.objects.all()
Out[4]: <QuerySet [<Flight: Flight object (1)>]>
```
3. Таким чином ми отримали, що у нас є один рейс під назвою Flight object (1). Це зовсім не інформативно. Виправляємо відповідь у середині models.py шляхом визначення функції __str__, що надасть вказівки щодо перетворення об’єкта Flight на рядок в середині класу:  
```python 
    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"
``` 
4. Далі буде приведено декілька прикладів:   
```python
# Створюємо змінну з назвою flights для збереження результатів запиту
In [7]: flights = Flight.objects.all()

# Показуємо всі рейси
In [8]: flights
Out[8]: <QuerySet [<Flight: 1: New York to London>]>

# Виокремлюємо лише перший рейс
In [9]: flight = flights.first()

# Виводимо інформацію про рейс
In [10]: flight
Out[10]: <Flight: 1: New York to London>

# Показуємо id рейсу
In [11]: flight.id
Out[11]: 1

# Показуємо пункт вильоту
In [12]: flight.origin
Out[12]: 'New York'

# Показуємо пункт призначення
In [13]: flight.destination
Out[13]: 'London'

# Показуємо тривалість рейсу
In [14]: flight.duration
Out[14]: 415
```

5. Але у нас вийшла не дуже гарна модель зберігання даних. Пам'ятаючи концепцію розглянуту раніше, переробимо класи у `models.py`  
```python
class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"

class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"
```
6. От же що ми зробили:  
- Вказали, що обидва поля `origin` і `destination` є зовнішніми ключами, тобто вони посилаються на інший об’єкт.  
- Подаючи `Airport` як наш перший аргумент, вказуємо тип об’єкта, до якого належить це поле.  
- Наступний аргумент `on_delete=models.CASCADE` надає вказівки щодо дій у разі, якщо аеропорт буде видалено. В цьому випадку ми вказуємо, що за видалення аеропорту всі пов’язані з ним рейси також повинні бути видалені. На додаток до CASCADE існує ще кілька альтернатив.  
- В `related name` ми надаємо пов’язане ім’я, яке дає нам змогу шукати всі рейси з цим аеропортом як пунктом вильоту чи призначення.  

7. Повторюємо пункти 2 та 4 попереднього розділу, щоб застосувати зміни.  Також потрібно видалити запис з БД, або сам файл БД, тому що він вже не відповідає структурі. 

8. Заповнимо нову структуру БД даними:

```python
# Імпортуємо всі моделі
In [1]: from flights.models import *

# Створюємо нові аеропорти
In [2]: jfk = Airport(code="JFK", city="New York")
In [4]: lhr = Airport(code="LHR", city="London")
In [6]: cdg = Airport(code="CDG", city="Paris")
In [9]: nrt = Airport(code="NRT", city="Tokyo")

# Зберігаємо аеропорти у базі даних
In [3]: jfk.save()
In [5]: lhr.save()
In [8]: cdg.save()
In [10]: nrt.save()

# Додаємо рейс та зберігаємо його до бази даних
f = Flight(origin=jfk, destination=lhr, duration=414)
f.save()

# Показуємо певну інформацію про рейс
In [14]: f
Out[14]: <Flight: 1: New York (JFK) to London (LHR)>
In [15]: f.origin
Out[15]: <Airport: New York (JFK)>

# Використовуємо релятивне ім’я для запиту за аеропортом призначення:
In [17]: lhr.arrivals.all()
Out[17]: <QuerySet [<Flight: 1: New York (JFK) to London (LHR)>]>

```
## Запуск застосунку
1. Зміни у файлі urls.py:
```python
urlpatterns = [
    path('', views.index, name="index"),
]
```
2. Додамо у файл views.py:
```python
from django.shortcuts import render
from .models import Flight, Airport

# Створюємо наші views.

def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })
```

3. Створюємо новий файл airline/flight/templates/flights/layout.html:

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Flights</title>
    </head>
    <body>
        {% block body %}
        {% endblock %}
    </body>
</html>
```

4. Створюємо у тій же теці index.html:

```html
{% extends "flights/layout.html" %}

{% block body %}
    <h1>Flights:</h1>
    <ul>
        {% for flight in flights %}
            <li>Flight {{ flight.id }}: {{ flight.origin }} to {{ flight.destination }}</li>
        {% endfor %}
    </ul>
{% endblock %}
```
5. Запустимо сервер:  
`python manage.py runserver`

6. За адресою `http://127.0.0.1:8000/flights` отримаємо наступну сторінку:  

![flights](.img/flights.jpg)

7. Додамо трохи більше інформації до наших даних:   

```python
# імпортуємо усі моделі
In: from flights.models import *

# Використовуємо команду filter для пошуку всіх аеропортів, розміщених у Нью-Йорку 
In: Airport.objects.filter(city="New York")
Out: <QuerySet [<Airport: New York (JFK)>]>

# Використовуємо команду get для виокремлення одного аеропорту у Нью-Йорку
In: Airport.objects.get(city="New York")
Out: <Airport: New York (JFK)>

# Призначаємо аеропортам назви змінних:
In: jfk = Airport.objects.get(city="New York")
In: cdg = Airport.objects.get(city="Paris")

# Створюємо та зберігаємо новий рейс:
In: f = Flight(origin=jfk, destination=cdg, duration=435)
In: f.save()

# Перевіримо результат:
In: Flight.objects.all()  
Out: <QuerySet [<Flight: 1: New York (JFK) to London (LHR)>, <Flight: 2: New York (JFK) to Paris (CDG)>]>
```
## Django Admin 
1. Уважно вивчаємо документацію по [вбудованому адміністративному інтерфейсу](https://docs.djangoproject.com/en/4.1/ref/contrib/admin/)  
2. Реєструємо користувача-адміністратора для використання цього інструмента:  
```shell
python manage.py createsuperuser
Username: vit
Email address: vit@um.com
Password: 
Password (again): 
Superuser created successfully.  
```
3. Імпортуємо до файлу admin.py нашого застосунку описані у models.py моделі:  
`from .models import Flight, Airport`  
4. Реєструємо моделі далі по тексту того ж файлу:  

```python
admin.site.register(Flight)
admin.site.register(Airport)
```
5. Запускаємо сайт, та заходимо за адресою: `http://127.0.0.1:8000/admin`  

![admin](.img/admin.jpg)  

6. От же ми отримуємо розроблений раніше інтерфейс керування даними нашого застосунку:  

![admin](.img/admin2.jpg) 

## Розбудова сайту 
1. Додамо посилання на Web-сторінку рейса при натисканні на нього, для чого створімо URL-шлях, що містить id рейсу:  

```python
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:flight_id>", views.flight, name="flight")
]
```
2. В views.py створимо функцію flight, що містить ідентифікатор рейсу та показує нову html-сторінку:  

```python
def flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    return render(request, "flights/flight.html", {
        "flight": flight
    })
```

3. Створимо шаблон сторінки `flights/flight.html` з інформацією про рейс та посиланням для повернення на домашню сторінку:  

```html
{% extends "flights/layout.html" %}

{% block body %}
    <h1>Flight {{ flight.id }}</h1>
    <ul>
        <li>Origin: {{ flight.origin }}</li>
        <li>Destination: {{ flight.destination }}</li>
        <li>Duration: {{ flight.duration }} minutes</li>
    </ul>
    <a href="{% url 'index' %}">All Flights</a>
{% endblock %}
```

4. Змінимо нашу головну сторінку, додавши посилання з кожного рейсу:  

```html
<li><a href="{% url 'flight' flight.id %}">Flight {{ flight.id }}</a>
```

5. Як результат отримуємо ось таку головну сторінку:  

![index](.img/index.jpg)  

6. Та наступну сторінку з інформацією про рейс при переході за посиланням:  

![id1](.img/page_id1.jpg)  

