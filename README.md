# Receipt checker Backend 

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/Fakhrillo/Receipt_Backend.git
$ cd Receipt_Backend
```

Create .env and add necessary environment variables (important one is `DJANGO_SECRET_KEY`)

Create a virtual environment to install dependencies in and activate it:

```sh
$ python3 -m venv env (python on Windows)
$ source env/bin/activate (env\Scripts\activate on Windows)
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `venv`.

Once `pip` has finished downloading the dependencies:
```sh
(env)$ python manage.py makemigrations && python manage.py migrate
(env)$ python manage.py createsuperuser (create super user to access admin page)
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/admin/`.

## Walkthrough

This is a very simple backend with Django for my previous project Receipt Checker project `https://github.com/Fakhrillo/Receipt_TgBot` here you can see the project it self.
I disabled unnecessary settings like DB and AWS credentials to test this project locally.

I used Django REST framework to create APIs and REST framework's JWTAuthentication to create tokens and authorization