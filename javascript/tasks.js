// Зачекати завантаження сторінки
document.addEventListener('DOMContentLoaded', function() {

    // Отримати кнопку надсилання та введення для подальшого використання 
    const submit = document.querySelector('#submit');
    const newTask = document.querySelector('#task');

    // За замовчуванням вимкнути кнопку надсилання:
    submit.disabled = true;

    // Слухати подію вводу даних до поля введення:
    newTask.onkeyup = () => {
        if (newTask.value.length > 0) {
            submit.disabled = false;
        }
        else {
            submit.disabled = true;
        }
    }

    // Слухати подію надсилання форми
    document.querySelector('form').onsubmit = () => {

        // Знайти завдання, яке додав користувач
        const task = newTask.value;

        // Створити пункт списку для нового завдання та додати завдання до нього
        const li = document.createElement('li');
        li.innerHTML = task;

        // Додати новий елемент до невпорядкованого списку:
        document.querySelector('#tasks').append(li);

        // Очистити поле введення:
        newTask.value = '';

        // Знову вимкнути кнопку надсилання:
        submit.disabled = true;

        // Зупинити надсилання форми:
        return false;
    }
});