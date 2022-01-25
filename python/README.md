# Contents

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
```
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
```
for i in range(6):
    print(i)
```
See in the [file](loops.py)

## Functions
```
def square(x):
    return x * x
```
See in the [file](functions.py)

## Modules
Дозволяють імпортувати функцію з іншого файла
```
from functions import square

print(f"The square of 5 is {square(5)}")
```
Або під'єднати увесь модуль
```
import functions

print(f"The squuare of 5 is {functions.square(5)}")
```

See in the files [square.py](square.py) and [functions.py](functions.py)


## [Go back](../README.md)

