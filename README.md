# space-industry

It is a web application based on Django
The backend use RabbitMQ and Celery workers to handle the periodic tasks
The frontend uses getbootstrap framework version 4.6 from getbootstrap.bom

Database is based on SQLite3 but can be replaced in production with postgresql or other

Development Install.

1. clone the repository (git clone https://....)
2. prepare a virtual environment with python 3.8 or above
3. activate the virtual environment
4. run pip install -r requirements.txt to install all the required python libraries
5. eventually run the migrations (python3 manage.py makemigrations && python3 manage.py migrations)
6. install RabbitMQ
7. open a python shell within the venv and install the nltk data:
import nltk
nltk.download("stopwords")

Execute the project.

1. open 4 terminals (yes, you need 4 of those, but you can certainly do better)
2. execute rabbitmq (if it does not start automatically as a service)
3. run the django server from one terminal (python3 manage.py runserver)
4. run the celery beat from another terminal (celery -A spaceindustry beat -l INFO)
5. run the celery worker from the last terminal (celery -A spaceindustry worker -B -l INFO)

Enjoy.

Open the web browser and connect to: http://127.0.0.1:8000/


Production Deployment.

Django / Python provide a webserver running but it is not ideal for production.
In our production environment we use nginx as a proxy service through unix.socket gunicorn.
Gunicorn workers are connected to django.

This all setup requires some attention and this readme does not intend to provide the recommendation about this. We suggest to review the following articles as really well written:
https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04
