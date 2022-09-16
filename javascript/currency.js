// document.addEventListener('DOMContentLoaded', function() {
//     // Надіслати запит GET до URL
//     fetch('https://api.apilayer.com/currency_data/live?source=USD&currencies=EUR,UAH&apikey=YOUR_ACCESS_KEY')
//     // Перетворити відповідь у формат json 
//     .then(response => response.json())
//     .then(data => {
//         // Вивести дані до консолі
//         console.log(data);
//     });
// });

document.addEventListener('DOMContentLoaded', function() {
    // Надіслати запит GET до URLL
    fetch('https://api.apilayer.com/currency_data/live?source=USD&currencies=EUR,UAH&apikey=YOUR_ACCESS_KEY')
    // Перетворити відповідь у формат json
    .then(response => response.json())
    .then(data => {

        // Отримати курс із отриманих даних
        const rate = data.quotes.USDUAH;

        // Вивести повідомлення на екран
        document.querySelector('body').innerHTML = `<h1>1 USD дорівнює  ${rate.toFixed(4)} UAH</h1>`;
    });
});