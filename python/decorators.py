# Декоратори для зміни поведінки функції.  Декоратор - це функція яка приймає іншу функцію як аргумент та повертає змінену версію цієї функуції. 
# Парадигма функціональого программування, де функція - це значення 

def announce(f):
    def wrapper():
        print("About to run the function...")
        f()
        print("Done with the function.")
    return wrapper

# Вище декоратор. Додаємо його за допомогою равлика до нової функції hello
@announce
def hello():
    print("Hello, world!")

hello()
