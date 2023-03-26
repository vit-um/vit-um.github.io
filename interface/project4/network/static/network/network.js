document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#all').addEventListener('click', () => load_posts('all'));
    document.querySelector('#following').addEventListener('click', () => load_posts('following'));

    load_posts('all');
});


function load_posts(filter) {
    // Show the posts and other views
    document.querySelector('#new_post').style.display = 'none';
    document.querySelector('#tab-panel').style.display = 'block';

    // Show the mailbox name
    if (filter === 'following') {
        document.querySelector('#following').setAttribute('class', 'tab active');
        document.querySelector('#all').setAttribute('class', 'tab');
    }
    else {
        document.querySelector('#following').setAttribute('class', 'tab');
        document.querySelector('#all').setAttribute('class', 'tab active');
    }
    document.querySelector('#tab-panel').innerHTML = '';

    // Получаем элемент p с id="current_user"
    const currentUser = document.getElementById('current_user');
    // Получаем значение атрибута data-username
    const curUser = currentUser.dataset.username;   
    console.log(curUser);

    fetch('/posts/' + filter)
    .then(response => response.json())
    .then(posts => {
        const posts_div = document.createElement('div');
    
        posts.forEach(post => {
            const post_div = document.createElement('div');
            post_div.setAttribute('id', 'post-block');
            const auth_field = document.createElement('span');
            auth_field.innerHTML = `${post.author[0]}`;
            auth_field.setAttribute('id', 'auth');
            const dt_field = document.createElement('span'); 
            dt_field.innerHTML = `${post.timestamp}`;
            dt_field.setAttribute('id', 'stamp');

            const post_field = document.createElement('div');
            post_field.setAttribute('id', 'text-block');
            post_field.innerHTML = `${post.post}`;

            const parent_div = document.createElement('parent_div');
            parent_div.setAttribute('id', 'button-block');
            const like_button = document.createElement('button');
            like_button.className = 'like-btn';
            const like_count = document.createElement('span');
            like_count.setAttribute('id', 'like-count'); 
            like_count.innerHTML = `${post.likes}`;
            
            if (post.author[0] === curUser) {
                const edit_button = document.createElement('button');
                edit_button.className = 'edit-btn';
                parent_div.append(edit_button, like_button, like_count);
            }
            else
                parent_div.append(like_button, like_count);

            post_field.append(parent_div)
            post_div.append(auth_field, dt_field, post_field);

            posts_div.append(post_div);
        });
        document.querySelector('#tab-panel').append(posts_div);
    });
}

