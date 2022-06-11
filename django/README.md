# Contents

## Install Django and create a new project
1. Install Django  
`pip install Django`  

2. Create the new project with name "myproject"  
`django-admin startproject myproject`   
`cd myproject`
3. Start work with the project on the server http://127.0.0.1:8000/  
`python manage.py runserver`

4. Create apps in the project, for example one, with name "hello"  
`python manage.py startapp hello`

5. Install the application in `myproject/myproject/settings.py`. To do this, add the application name to the `INSTALLED_APPS` list:  
```python
# Application definition
INSTALLED_APPS = [
    'hello',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```
## Configure the application
1. Go to `myproject\hello\views.py` and add http response cod 200 and our text  
```python
from django.http import HttpResponse
# Create your views here.
def index(request): 
    return HttpResponse("Hello, world!")
```  
2. We already have the urls.py file for the whole project, but it's best to have separate files for each application.  Create a file: `myproject\hello\urls.py` and add this path to it:  

```python  
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index")
]
```  
3. Include all paths from the `urls.py` file in our application. To do this, we will write: `include ("APP_NAME.urls")`, where `include` is a function that we access by importing `include` from `django.urls` as shown in `urls.py`  
```python  
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', include("hello.urls"))
]

```  
## Create [Templates](https://docs.djangoproject.com/en/4.0/topics/templates/) to write HTML and CSS to separate files  

1. Create a file and path: `myproject\hello\templates\hello\index.html`  
2. Add the following code to the file:
```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Hello</title>
    </head>
    <body>
        <h1>Hello, World!</h1>
    </body>
</html>
```  
3. Add the following code to `myproject\hello\views.py`:
```python  
def index(request):
    return render(request, "hello/index.html")
```  
4. Change the contents of our HTML files depending on the URL visited using the `greet` function:  
```python 
def greet(request, name):
    return render(request, "hello/greet.html", {
        "name": name.capitalize()
    })
```  
5. Add the following code to `myproject\hello\templates\hello\greet.html`  
```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Hello</title>
    </head>
    <body>
        <h1>Hello, {{ name }}!</h1>
    </body>
</html>
```  
6. Add [datetime](https://docs.python.org/3/library/datetime.html) Python function
```  
> python
Python 3.10.2 (tags/v3.10.2:a58ebcc, Jan 17 2022, 14:12:15) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import datetime
>>> now = datetime.datetime.now()
>>> now.day
11
>>> now.month
6
>>> now.year
2022
>>> exit()
```  
7. Add logic in `myproject\hello\views.py`:
```python 
import datetime
def index(request):
    now = datetime.datetime.now()
    return render(request, "hello/index.html", {
        "newyear": now.month == 1 and now.day == 1
    })
```  

8. Add conditions in html  
```html
    <body>
        {% if newyear %}
            <h1>YES</h1>
        {% else %}
            <h1>NO</h1>
        {% endif %}
    </body>
```  

## Style templates
1. Add a static file and path `myproject\hello\static\hello\styles.css`
2. Add content in the file: 
```html
h2 {
    color: red;
    font-family: sans-serif;
    font-size: 50px;
    text-align: center;
}
```  
3. Add the code `{% load static %}` at the top of the html file  
4. Add a css style sheet to the html file header  
`<link rel="stylesheet" href="{% static 'hello/styles.css' %}">`



## [Go back](../README.md)

