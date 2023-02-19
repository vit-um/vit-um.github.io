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
  const recipients = document.querySelector('#compose-recipients');
  recipients.value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  const submit = document.querySelector('.subm-disable');


  // Забороняємо натискання кнопки Надіслати" в разі якщо довжина введеної адреси менше 3 символів
  submit.disabled = true;
  recipients.onkeyup = () => {
    if (recipients.value.length > 3) 
      submit.disabled = false;
    else 
      submit.disabled = true;
    }
  
  // Після відправки форми з новим листом викликаємо обробник, функуцію sendmail
  document.querySelector('#compose-form').onsubmit = () => sendmail();

  return false
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
  switch(mailbox) {
    case 'sent':
      document.querySelector('#emails-view').innerHTML = `<h3>Надіслані листи</h3>`;
      break;
    case 'archive':
      document.querySelector('#emails-view').innerHTML = `<h3>Архівовані листи</h3>`;
      break;
    default:
      document.querySelector('#emails-view').innerHTML = `<h3>Вхідні листи</h3>`;
  } 
  
  fetch('/emails/' + mailbox)
  .then(response => response.json())
  .then(emails => {
    const mailbox_div = document.createElement('div');
    mailbox_div.setAttribute('id', 'mailsblock');

    emails.forEach(email => {
      const letter_div = document.createElement('div');
      const address_field = document.createElement('span');
      const arch_button = document.createElement('button');

      if (mailbox === 'sent') {
        if (email.read === true)
          letter_div.setAttribute('class', 'mailgrid_sent read');
        else
          letter_div.setAttribute('class', 'mailgrid_sent unread');
        address_field.innerHTML = `Кому: ${email.recipients}`;
      }
      else {
        address_field.innerHTML = `${email.sender}`;
        if (email.read === true)
          letter_div.setAttribute('class', 'mailgrid read');
        else
          letter_div.setAttribute('class', 'mailgrid unread');

        if (mailbox === 'inbox')
          arch_button.className = 'archButton';
        else
          arch_button.className = 'unarchButton';
      }
      
      const subject_field = document.createElement('span');
      subject_field.innerHTML = `${email.subject}`;

      const datatime_field = document.createElement('span');
      datatime_field.innerHTML = `${email.timestamp}`;
      datatime_field.setAttribute('class', 'stamp');


      const linkdiv = document.createElement('div');
      linkdiv.setAttribute('class', 'linkdiv');

      if (mailbox === 'sent')
        letter_div.append(address_field, subject_field, datatime_field, linkdiv);
      if (mailbox === 'inbox')
        letter_div.append(arch_button, address_field, subject_field, datatime_field, linkdiv);
      if (mailbox === 'archive')
        letter_div.append(arch_button, address_field, subject_field, datatime_field, linkdiv);

      mailbox_div.append(letter_div);

      linkdiv.addEventListener('click', () => {
        readmail(email.id);
      });
    
      arch_button.addEventListener('click', () => {
        archive_email(email.id, email.archived);
      });

    });

    document.querySelector('#emails-view').append(mailbox_div);

  });
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
      if (result.error) {
          document.querySelector('#error').setAttribute('class', "alert alert-danger");
          document.querySelector('#error').innerHTML = `${result.error}`;
          compose_email();
      }
      else {
          load_mailbox('sent');
      }
  });

  return false;
}

function readmail(id) {

  document.querySelector('#mailsblock').remove();
 
  
  fetch('/emails/' + id)
  .then(response => response.json())
  .then(email => {
  
    document.querySelector("h3").innerHTML = `${email.subject}`;

    const divLetter = document.createElement('div');

    const grid_div = document.createElement('div');
    grid_div.setAttribute('id', 'grid');
    
    const sender_field = document.createElement('div');
    sender_field.setAttribute("style","text-align: left;");
    sender_field.innerHTML = `<strong>Від:</strong> ${email.sender}`;

    const datatime_field = document.createElement('div');
    datatime_field.setAttribute("style", "text-align: right;");
    datatime_field.innerHTML = `${email.timestamp}`;

    grid_div.append(sender_field, datatime_field);


    const recipients_field = document.createElement('p');
    recipients_field.innerHTML = `<strong>Кому:</strong> ${email.recipients}`;

    const body_field = document.createElement('p');
    const text = email.body.split("\n");
    let body = '';
    for (let unit of text) {
        body += unit + '<br>'
    }

    body_field.innerHTML = body;

    const reply_btn = document.createElement('button');
    reply_btn.innerText = 'Відповісти';
    reply_btn.className = 'btn btn-outline-primary';

    divLetter.append(grid_div, recipients_field, body_field, reply_btn);
    document.querySelector('#emails-view').append(divLetter);

    reply_btn.addEventListener('click', () => reply_email(email));
    
  });

  // Позначимо відкритий лист прочитаним
  fetch('/emails/'+ id, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
  });
  
}


function archive_email(mailID, archStatus) {
  fetch('/emails/'+ mailID, {
      method: 'PUT',
      body: JSON.stringify({
        archived: !archStatus
      })
  })
  .then(() => {
        load_mailbox('inbox')
  });   
}


function reply_email(email) {

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  document.querySelector('#compose-recipients').value = email.sender;

  if (email.subject.slice(0,4) == 'Re: ') 
      document.querySelector('#compose-subject').value = email.subject;
  else 
      document.querySelector('#compose-subject').value = 'Re: ' + email.subject;
  
  const text = email.body.split("\n");
  let body = '';
  for (let unit of text) {
      body = body + '>' + unit + '\n';
  }
  
  document.querySelector('#compose-body').value = `\n${email.timestamp} ${email.sender} пише:\n` + body;

  document.querySelector('#compose-form').onsubmit = () => sendmail();
}
