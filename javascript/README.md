# JavaScript

## Теги додавання JavaScript до коду сторінки   
```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Привіт</title>
        <script>
            alert('Привіт, світ!');
        </script>
    </head>
    <body>
        <h1>Hello!</h1>
    </body>
</html>
```
## Події. Подійно-орієнтоване програмування.
Будь яка дія зроблена користувачем на сайті може оброблятися кодом як окрема подія. Реакцію на ту чи іншу подію зручно обробляти функціями написаними на [JavaScript](https://www.w3schools.com/js/default.asp).  
1. От же перетворимо наше сповіщення на сайті в окрему функцію:    
```html
function hello() {
    alert('Привіт, світ!')
}
```
2. Наступним рядком описуємо HTML-кнопку з атрибутом `onclick`, який дає вказівки браузеру викликати нашу функцію при натисканні на неї:  
```html
<button onclick="hello()">Click Here</button>
```
3. Код сторінки буде виглядати тепер наступним чином:  
```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Привіт</title>
        <script>
            function hello() {
                alert('Привіт, світ!');
            }
        </script>
    </head>
    <body>
        <h1>Hello!</h1>
        <button onclick="hello()">Click Here</button>
    </body>
</html>
```
## Змінні.
1. Є три ключові слова, які ми можемо використовувати для присвоєння значень у JavaScript:  
- `var` - використовується для глобального визначення змінної: `var age = 20;`  
- `let` - використовується для визначення змінної, область видимості якої обмежена поточним блоком, таким як функція або цикл: `let counter = 1;`  
- `const` - використовується для визначення значення, яке не зміниться: `const PI = 3.14;`  

2. Для виводу змінної проміж тексту використовуємо наступний синтаксис `` `Text ${var}` ``  

3. Для прикладу того, як ми можемо використовувати змінні, розробимо простий лічильник:  

```html
<!DOCTYPE html>
<html lang="uk">
    <head>
        <title>Обрахунок</title>
        <script>
            let counter = 0;
            function count() {
                counter++;
                alert(counter);
            }
        </script>
    </head>
    <body>
        <h1>Привіт!</h1>
        <button onclick="count()">Порахувати</button>
    </body>
</html>
```
