document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  // Зверніть увагу, що після завантаження DOM сторінки, ми прикріплюємо слухачі подій до кожної кнопки. 
  // Наприклад, коли натиснуто кнопку inbox ми викликаємо функцію load_mailbox з аргументом 'inbox'; 
  // після натискання кнопки compose ми викликаємо функцію compose_email.

  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
// Функція compose_email спочатку приховує emails-view (встановивши його 
// властивість style.display як none) і показує compose-view (встановивши 
// його властивість style.display як block). A після цього функція забирає 
// все, що було в полях введення (де користувач може ввести електронну адресу 
// отримувача, тему і тіло листа), і встановлює їхні значення як пустий рядок '' 
// щоб очистити ці поля. Це означає, що щоразу, як ви натискаєте кнопку «Написати», 
// ви маєте отримувати пусту форму написання листа: ви можете перевірити це, 
// увівши якісь значення у форму, переключивши на «Вхідні», а потім повернувшись до «Написати».

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Після відправки форми з новим листом викликаємо обробник, функуцію sendmail
  document.querySelector('#compose-form').onsubmit = () => sendmail();

}

function load_mailbox(mailbox) {
// Функція load_mailbox, тим часом, спочатку показує emails-view а потім приховує compose-view. 
// Функція load_mailbox також приймає аргумент, що буде іменем теки з поштою, яку користувач пробує переглянути. 
// Для цього проєкту ви створите поштовий клієнт з трьома теками – «Вхідні» (inbox), «Надіслані» (sent) 
// з усіма надісланими листами і «Архів» (archive) з листами, що були колись в теці «Вхідні», але пізніше їх було заархівовано. 
// Таким чином, аргумент для load_mailbox, буде одним із цих трьох значень, і функція load_mailbox 
// відобразить назву вибраної теки завдяки оновленню innerHTML у emails-view (із заміною першої літери на велику.) 
// Ось чому після вибору певної теки з листами у браузері ви бачите, що назва цієї теки (з великої літери) з’являється у DOM:
// функція load_mailbox оновлює emails-view, щоб включити необхідний текст.
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

}


function sendmail() {
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.getElementById("compose-recipients").value,
        subject: document.getElementById("compose-subject").value,
        body: document.getElementById("compose-body").value
    })
  })
  .then(response => response.json())
  .then(result => {
      // Вивести результат в консоль
      console.log(result);
      if (result.error) {
          document.querySelector('#error').setAttribute('class', "alert alert-danger fade show");
          document.querySelector('#error').innerHTML = `${result.error}`;
          compose_email();
      }
      else {
          // document.querySelector('#error').setAttribute('class', "alert alert-success fade show");
          // document.querySelector('#error').innerHTML = `${result.error}`;
//          load_mailbox('sent');
      }
  });

  return false;
}


// https://getbootstrap.com/docs/5.2/components/alerts/#dismissing  
// <div class="alert alert-success fade show" role="alert"> </div>
