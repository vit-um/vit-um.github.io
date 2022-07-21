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
