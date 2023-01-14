
# MySite-Django

A simple personal website with projects, and have features like `user management`, `score`, `pushing notifications`, `admin logs`, `API` and many other things. You can `hide your secrets` like pushbullet ID in the admin panel. The project is live in [LINK](https://jerit.ml)


## Authors

- [Jerit Baiju](https://github.com/Jerit-Baiju/)
- [Jojit Thomas](https://github.com/Jojit-Thomas)


## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/Jerit-Baiju/MySite-Django.git
$ cd MySite-Django
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ python3 -m venv env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `venv`.

Once `pip` has finished downloading the dependencies:
```sh
(env)$ python manage.py migrate
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`

To create a superuser:

```sh
(env)$ python manage.py createsuperuser
```
## Tech Stack

**Client:** HTML, JS, CSS

**Server:** PYTHON, DJANGO


## License

[MIT](https://github.com/Jerit-Baiju/MySite-Django/blob/master/LICENSE)
