function showPage(page) {

    // Сховати всі div: Вибираємо всі дів, а потім до кожну з них приховуємо.
    document.querySelectorAll('div').forEach(div => {
        div.style.display = 'none';
    });

    // Показати div, переданий у аргументі функції
    document.querySelector(`#${page}`).style.display = 'block';
}

// Зачекати завантаження сторінки:
document.addEventListener('DOMContentLoaded', function() {

    // Обрати всі кнопки
    document.querySelectorAll('button').forEach(button => {

        // Коли кнопку натиснуто, перейти на сторінку. Функція this - Стосуєстья будь якого елементу DOM, що отримав подію. Отже з масиву  dataset обирається арибут відповідної кнопки
        button.onclick = function() {
            showPage(this.dataset.page);
        }
    })
});
