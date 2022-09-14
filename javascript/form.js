document.addEventListener('DOMContentLoaded', function() {   
    document.querySelector('form').onsubmit = function() {
        const name = document.querySelector('#name').value;
        alert(`Привіт, ${name}`);
        // document.querySelector('h1').innerHTML = `Привіт, ${name}`;
    }
});

