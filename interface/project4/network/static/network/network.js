document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#all').addEventListener('click', () => load_posts('all'));
    document.querySelector('#following').addEventListener('click', () => load_posts('following'));

    load_posts('all');
});


function load_posts(filter) {
    
    // Получаем элемент p с id="current_user"
    const currentUser = document.getElementById('current_user');
    // Получаем значение атрибута data-username
    const curUser = currentUser.dataset.username;   
    // console.log(curUser);


    // Show the posts and other views
    if (curUser) {
        // Користувач авторизований
        document.querySelector('#new_post').style.display = 'block';  
    } else {
        // Користувач не авторизований
        document.querySelector('#new_post').style.display = 'none'; 
        document.querySelector('.tab-list').style.display = 'none';  
    }
    document.querySelector('#tab-panel').style.display = 'block';

    // Забороняємо натискання кнопки Надіслати" в разі якщо довжина посту менше за 5 символів 
    const submit = document.querySelector('.subm-disable');
    const text = document.querySelector('#compose-body');
    text.value = '';
    submit.disabled = true;
    text.onkeyup = () => {
        if (text.value.length > 5) 
            submit.disabled = false;
        else 
            submit.disabled = true;
    }

    // Викликаємо функцію обробник натискання на кнопку Надіслати. 
    document.querySelector('#compose-form').onsubmit = () => send_post(filter);


    // Позначаємо активну вкладку 
    if (filter === 'following') {
        document.querySelector('#following').setAttribute('class', 'tab active');
        document.querySelector('#all').setAttribute('class', 'tab');
    }
    else {
        document.querySelector('#following').setAttribute('class', 'tab');
        document.querySelector('#all').setAttribute('class', 'tab active');
    }
    document.querySelector('#tab-panel').innerHTML = '';

    fetch('/posts/' + filter)
    .then(response => response.json())
    .then(posts => {
        const posts_div = document.createElement('div');
    
        posts.forEach(post => {
            const post_div = document.createElement('div');
            post_div.setAttribute('id', 'post-block');
            
            // Автор допису та його дата
            const auth_field = document.createElement('span');
            auth_field.setAttribute('id', 'auth');
            
            const link = document.createElement('a');
            // link.setAttribute('href', '/user/' + `${post.author[0]}`); //розкоментувати для отримання JSON-відповіді на екрані
            link.innerHTML = `${post.author[0]}`;
            link.setAttribute('style', 'cursor: pointer;');

            auth_field.append(link);

            const dt_field = document.createElement('span'); 
            dt_field.innerHTML = `${post.timestamp}`;
            dt_field.setAttribute('id', 'stamp');

            link.addEventListener('click', () => {
                profile_settings(post.author);
            });

            // Текст або тіло допису
            const post_field = document.createElement('div');
            post_field.setAttribute('id', `text-block-${post.id}`);
            post_field.innerHTML = convert_to_HTML(post.post);

            // Рядок з елементами керування дописом
            const parent_div = document.createElement('div');
            parent_div.setAttribute('id', 'button-block');
            
            const like_count = document.createElement('span');
            like_count.setAttribute('id', 'like-count'); 
            like_count.innerHTML = `${post.likes}`;

            let liker = 0;
            let count = post.likes;
            const like_button = document.createElement('button');
            if (post.users_like.includes(curUser)) {
                // Якщо масив містить елемент curUser
                like_button.className = 'like-btn';
                liker = -1;
            } else {
                // Якщо масив не містить елемент curUser
                like_button.className = 'unlike-btn';
                liker = 1;
            }
            like_button.addEventListener('click', () => {
                count_like(post.id, liker);
                if (liker === 1) {
                    like_button.className = 'like-btn';
                    count++;
                    like_count.innerHTML = `${count}`;
                    liker = -1
                } else {
                    like_button.className = 'unlike-btn';
                    count--;
                    like_count.innerHTML = `${count}`;
                    liker = 1
                }
            });
            

            if (post.author[0] === curUser) {
                const edit_button = document.createElement('button');
                edit_button.className = 'edit-btn';
                parent_div.append(edit_button, like_button, like_count);

                edit_button.addEventListener('click', () => {
                    // Визначення та копіювання тексту посту для редагування  
                    const postArea = document.querySelector(`#text-block-${post.id}`);
                    const postText = postArea.innerText;
                    postArea.innerHTML = '';
                    // Створення нової тестової області для редагування тексту, та копіювання в нього тексту посту з обрізкою зайвих символів в кінці
                    const newTextArea = document.createElement('textarea');
                    newTextArea.setAttribute('class', `editTextArea editTextArea-${post.id}`);
                    newTextArea.innerHTML = postText.trim();
                    post_field.appendChild(newTextArea);
            
                    // Приховуємо зайві елементи керування: edit and like button temporarily
                    like_button.style.display = 'none';
                    edit_button.style.display = 'none';
                    like_count.style.display = 'none';

                    // Створюємо кнопку та слухача події її натискання для відміни режиму редагування 
                    const CancelButton = document.createElement('button');
                    CancelButton.className = 'btn btn-primary';
                    CancelButton.innerHTML = 'Скасувати';

                    CancelButton.addEventListener('click', () => {
                        newTextArea.remove();
                        CancelButton.remove();
                        SubmitButton.remove();
                        postArea.innerHTML = convert_to_HTML(postText);
                        like_button.style.display = 'inline-block';
                        edit_button.style.display = 'inline-block';
                        like_count.style.display = 'inline-block';
                    });

                    // Створюємо кнопку та слухача події її натискання для зберігання виправленого посту в базі
                    const SubmitButton = document.createElement('button');
                    SubmitButton.className = 'btn btn-primary';
                    SubmitButton.innerHTML = 'Зберегти';
                    parent_div.append(CancelButton, SubmitButton);

                    SubmitButton.addEventListener('click', () => {
                        const newTextArea = document.querySelector(`.editTextArea-${post.id}`);
                        const newText = newTextArea.value.trim();
                        console.log(newText);
                        if (newText) {
                            fetch(`/post/${post.id}`, {
                                method: 'PUT',
                                body: JSON.stringify({
                                    post: newText,
                                })
                            })
                            .then(response => response.json())
                            .then(result => {
                                if (result.success) {
                                    newTextArea.remove();
                                    CancelButton.remove();
                                    SubmitButton.remove();
                                    postArea.innerHTML = convert_to_HTML(newText);
                                    like_button.style.display = 'inline-block';
                                    edit_button.style.display = 'inline-block';
                                    like_count.style.display = 'inline-block';
                                } else {
                                    alert(result.error);
                                }
                            });
                        }
                    });
                });
            }
            else
                parent_div.append(like_button, like_count);

            //post_field.append(parent_div)
            post_div.append(auth_field, dt_field, post_field, parent_div);

            posts_div.append(post_div);
        });
        document.querySelector('#tab-panel').append(posts_div);
    });
}

function profile_settings(user_profile) {
    
    document.querySelector('#new_post').style.display = 'none';
    document.querySelector('.tab-list').style.display = 'none';  
    document.querySelector('#tab-panel').style.display = 'block';
    document.querySelector('#tab-panel').innerHTML = '<h1>Сторінка профілю користувача</h1><br>' 
                + '<h5>Логін: ' +`${ user_profile[0] }` + '</h5>'
                + '<h5>Ім`я: ' +`${ user_profile[1] }` + '</h5>'
                + '<h5>Прізвище: ' +`${ user_profile[2] }` + '</h5><br>';


    fetch('/user/' + user_profile[0])
    .then(response => response.json())
    .then(data => {
        const { user, f_users, followers, following, posts } = data;
        const posts_div = document.createElement('div');
        posts_div.innerHTML = '<h5>Кількість підписників цього користувача: <span style="color:red;">' + `${followers}` +'</span></h5>'
                            + '<h5>Кількість осіб, за якими стежить цей користувач: <span style="color:red;">' + `${following}` +'</span></h5><br>';


        // Рядок з елементами керування
        const control_div = document.createElement('div');
        control_div.setAttribute('id', 'control-block');
                
        const exit_button = document.createElement('button');
        exit_button.innerHTML = 'Вийти';
        exit_button.className = 'btn btn-primary'

        exit_button.addEventListener('click', () => {
            load_posts('all');
        });

        const subs_button = document.createElement('button');
        subs_button.className = 'btn btn-primary'
        const containsUser = f_users.some(usr => usr.following.includes(user_profile[0]));
        console.log(containsUser);
        console.log(f_users[0].following);
        var subscriber = true;
        if (containsUser) {
            subs_button.innerHTML = 'Відписатись';
            subscriber = false;
        } else {
            subs_button.innerHTML = 'Підписатись';
            subscriber = true;
        }

        subs_button.addEventListener('click', () => {
            fetch('/user/'+ user_profile[0], {
                method: 'PUT',
                body: JSON.stringify({
                    subscriber: subscriber,
                })
            });   
            profile_settings(user_profile);
        });
        
        if (user === user_profile[0]) {
            control_div.append(exit_button);
        } else {
            control_div.append(subs_button, exit_button);
        }
        

        const name_head = document.createElement('h5');
        name_head.innerHTML = '<br>Усі дописи користувача <span style="color:red;">' + user_profile[0] +'</span> (' + user_profile[1] + ' ' + user_profile[2] + ')';

        posts_div.append(control_div, name_head);

        posts.forEach(post => {
            const dt_field = document.createElement('span'); 
            dt_field.innerHTML = `${post.timestamp}`;
            
            const post_div = document.createElement('div');
            post_div.setAttribute('id', 'post-block');

            // Текст або тіло допису
            const post_field = document.createElement('div');
            post_field.setAttribute('id', 'text-block');
            post_field.innerHTML = convert_to_HTML(post.post);

            post_div.append(post_field);

            posts_div.append(dt_field, post_div);
        });
        document.querySelector('#tab-panel').append(posts_div);
    });
    return false;
}

function send_post(filter) {
    fetch('/post', {
    method: 'POST',
    body: JSON.stringify({
        body: document.getElementById("compose-body").value
    })
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) {
            document.querySelector('#error').style.display = 'block';
            document.querySelector('#error').setAttribute('class', "alert alert-danger");
            document.querySelector('#error').innerHTML = `${result.error}`;
            setTimeout(function() {
                document.querySelector('#error').style.display = 'none';
            }, 5000);  
            load_posts(filter);
            
        }
        else {
            document.querySelector('#error').style.display = 'block';
            document.querySelector('#error').setAttribute('class', "alert alert-success");
            document.querySelector('#error').innerHTML = `${result.message}`;
            setTimeout(function() {
                document.querySelector('#error').style.display = 'none';
            }, 3000);  
            load_posts(filter);
        }
    });
    return false;
}


function convert_to_HTML(text) {
    let body = '';
    for (let unit of text.split("\n")) {
        body += unit + '<br>'
    }
    return body;
}


function count_like(postID, liker) {
    fetch('/post/'+ postID, {
        method: 'PUT',
        body: JSON.stringify({
            liker: liker,
        })
    });
}
