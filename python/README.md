# The Basics of the Python Language

## Type of variables

```
`int:` ціле число
`float:` число з рухомою комою
`chr:` окремий символ
`str:` рядок або послідовність символів
`bool:` булевий вираз, який може бути True (істинний) або False (хибний)
`NoneType:` Спеціальне значення (None), яке вказує на відсутність значення

```
## Conditions
```python
n = int(input("Number: "))

if n > 0:
	print("n is positive")
elif n < 0:
	print("n is negative")
else:
	print("n is zerro")
```
See in the [file](conditions.py)

## Types of Python Sequences

- [Strings](sequences.py) `"Harry"`
- [Lists](sequences.py) `[10, 100, 30, 40]` or `["Harry", "Ron", "Hermione", "Ginny"]` (список або послідовність змінних значень)
- [Tuples](sequences.py) `(10.0, 20.0)` (кортеж або послідовність незмінних значень)
- [Dictionary](dictionary.py) `{"Harry":"Gryffindor", "Draco": "Slytherin"}` (словник або збірка пар ключ-значення)
- [Sets](sets.py) `s = set()` (множина або набір унікальних значень)

## Loops
```python
for i in range(6):
    print(i)
```
See in the [file](loops.py)

## Functions
```python
def square(x):
    return x * x
```
See in the [file](functions.py)

## Modules
Дозволяють імпортувати функцію з іншого файла
```python
from functions import square

print(f"The square of 5 is {square(5)}")
```
Або під'єднати увесь модуль
```python
import functions

print(f"The squuare of 5 is {functions.square(5)}")
```
See in the files [square.py](square.py) and [functions.py](functions.py)

## Classes
Класи: ми вже бачили кілька різних типів змінних у Python, але як бути, якщо ми хочемо створити власний тип? Клас Python – це, по суті, шаблон для об’єкта нового типу, який може зберігати інформацію та виконувати дії. Ось клас, який визначає двовимірну точку:
```python
class Point():
    # Метод визначає, як створювати точку:
    def __init__(self, x, y):
        self.x = x
        self.y = y
```
More code see in [classes.py](classes.py)

## Decorators
Декоратори використовують для зміни поведінки функції.  Декоратор - це функція яка приймає іншу функцію як аргумент та повертає змінену версію цієї функуції.  
Парадигма функціональого программування, де функція - це значення 
```python
def announce(f):
    def wrapper():
        print("About to run the function...")
        f()
        print("Done with the function.")
    return wrapper

@announce
def hello():
    print("Hello, world!")

hello()
```
See in the file [decorators.py](decorators.py)

## Lambda
Лямбда-функції забезпечують ще один спосіб створення функцій у Python. Наприклад, якщо ми хочемо визначити ту саму функцію square, що і раніше, ми можемо написати:
```python
square = lambda x: x * x
```
Де аргументи йдуть ліворуч від :, а результат праворуч.  
Функцію зручно використовувати для сортування даних зі складною структурою, дивись приклад у файлі [lambda.py](lambda.py)

## Exceptions
When an error occurs, or exception as we call it, Python will normally stop and generate an error message.
```python
import sys

try:
    x = int(input("x: "))
    y = int(input("y: "))
except ValueError:
    print("Error: Invalid input.")
    sys.exit()
```
More code see in [exceptions.py](exceptions.py)

## Share your Wi-Fi password with your guests by printing it as qr code
1. Install two dependencies:  
```
pip install pillow  
pip install qrcode  
```  

2. Run this command:  
```
echo "WIFI:T:WPA;S:NETWORK_NAME;P:PASSWORD_HERE;H:;" | qr --output=wifi.png
```
3. Print this qr code  

![wifi](wifi.png)  

## [Go back](../README.md)

