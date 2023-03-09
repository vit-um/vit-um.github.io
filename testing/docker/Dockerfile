FROM python:3
COPY .  /usr/src/app
WORKDIR /usr/src/app
RUN pip install django
RUN pip install pillow
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]