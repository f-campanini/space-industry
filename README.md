# space-industry

It is a web application based on Django
The backend use RabbitMQ and Celery workers to handle the periodic tasks

Database is based on SQLite3 but can be replaced with postgresql or other

Install.

1. clone the repository (git clone https://....)
2. prepare a virtual environment with python 3.8 or above
3. activate the virtual environment
4. run pip install -r requirements.txt to install all the required python libraries
5. eventually run the migrations (python3 manage.py makemigrations && python3 manage.py migrations)
6. install RabbitMQ

Execute the project.

1. open 4 terminals (yes, you need 4 of those, but you can certainly do better)
2. execute rabbitmq (if it does not start automatically as a service)
3. run the django server from one terminal (python3 manage.py runserver)
4. run the celery beat from another terminal (celery -A spaceindustry beat -l INFO)
5. run the celery worker from the last terminal (celery -A spaceindustry worker -B -l INFO)

Enjoy.

Open the web browser and connect to: http://127.0.0.1:8000/
