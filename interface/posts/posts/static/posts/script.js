// Почати з першого допису
let counter = 1;

// Завантажувати 20 дописів за раз
const quantity = 20;

// Коли DOM завантажено, вивести перші 20 дописів
document.addEventListener('DOMContentLoaded', load);

// Якщо користувач дійшов кінця сторінки, завантажити наступні 20 дописів
window.onscroll = () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        load();
    }
};

// Завантажити наступну частину дописів
function load() {

    // Встановити початкову та кінцеву кількість дописів, потім оновити лічильник
    const start = counter;
    const end = start + quantity - 1;
    counter = end + 1;

    // Отримати нові дописи та додати на сторінку
    fetch(`/posts?start=${start}&end=${end}`)
    .then(response => response.json())
    .then(data => {
        data.posts.forEach(add_post);
    })
};

// Додати нові дописи до контенту в DOM
function add_post(contents) {

    // Створити новий допис
    const post = document.createElement('div');
    post.className = 'post';
    post.innerHTML = contents;

    // Додати допис до DOM
    document.querySelector('#posts').append(post);
};