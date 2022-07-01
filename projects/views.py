import random
import requests
from base.views import log
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages

# Create your views here.


def projects(request):
    log(request, 'Projects')
    projects = [
        {'name': 'Weather App', 'info': 'A project to get weather from all places, working by scrapping data from GOOGLE WEATHER.',
            'src': '/projects/weather', 'btn': 'Go'},
        {'name': 'PyFlit', 'info': 'Tool for adding components and pages in FLASK. Can be used to send PYTHON variables to JAVASCRIPT.',
            'src': 'https://pypi.org/project/pyflit/', 'btn': 'PYPI'},
        {'name': 'Clara', 'info': 'CHAT-BOT made with ELIO-BOT-API. Simple STATIC Project.',
            'src': '/projects/clara', 'btn': 'Chat'},
        {'name': 'MySite', 'info': 'DYNAMIC WEBSITE made with DJANGO framework, FEATURES - Admin Panel, User Management, User-Score Handling, LOGS, etc.. ',
            'src': 'https://github.com/jerit-baiju/mysite-django', 'btn': 'GitHub'},
        {'name': 'Number Game', 'info': 'You should assume the number that is picked from 0-100 randomly by computer with TEN chances.',
            'src': '/projects/num_game', 'btn': 'Play'},
        {'name': 'Elio Bot API', 'info': 'This API provides you free commands, wikipedia support, user detection.',
            'src': 'https://github.com/jerit-baiju/chat_bot_api', 'btn': 'GitHub'},
        {'name': 'GitHub Activity Generator', 'info': 'Python script for creating commits, can specify number of commits, code consistency, and many more.',
            'src': 'https://github.com/jerit-baiju/activity_generator', 'btn': 'GitHub'}

    ]
    random.shuffle(projects)
    context = {
        'title': 'Projects | Jerit Baiju',
        'projects': projects,
        'page': 'projects'
    }
    return render(request, 'projects/projects.html', context)


@login_required(login_url='login-page')
def clara(request):
    log(request, 'Clara')
    context = {
        'title': 'Clara | Jerit Baiju',
        'name': request.user.first_name,
    }
    return render(request, 'projects/clara.html', context)


def num_Game(request):
    if request.user.score == None:
        score = 0
    else:
        score = request.user.score

    if request.method == 'POST':
        context = {
            'score': score,
            'win': True,
            'dark': True,
            'title': 'Number Game'
        }
        return render(request, 'projects/num_game.html', context)
    else:
        log(request, 'Num Game')
        context = {
            'score': score,
            'title': 'Number Game',
            'randint': random.randint(0, 100),
            'dark': True
        }
        return render(request, 'projects/num_game.html', context)


@login_required(login_url='login-page')
def num_Game_add(request):
    if request.user.is_authenticated:
        if request.user.score == None:
            score = 0
        else:
            score = request.user.score
        request.user.score = score + 5
        request.user.save()
        log(request, 'scored')
        return redirect('num-game')
    else:
        messages.error(request, 'Please login to add your score.')
        return redirect('num-game')


def weather(request):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }
    context = {
        'title': 'Weather App',
        'dark': True
    }
    if request.method == 'POST':
        def get_weather(city):
            try:
                url = f"https://www.google.com/search?q=weather+in+{city}"
                page = requests.get(url, headers=headers)
                soup = BeautifulSoup(page.content, 'html.parser')
                temperature = soup.find('span', attrs={'id': 'wob_ttm'}).text
                status = soup.find('span', attrs={'id': 'wob_dc'}).text
                location = soup.find('div', attrs={'id': 'wob_loc'}).text
                temperature_op = (f"{temperature} °F \n")
                status_op = (f"Status - {status} \n")
                src = soup.find('img', attrs={'id': 'wob_tci'}).get('src')
                day = soup.find('div', attrs={'id': 'wob_dts'}).text
                context = {'tmp': temperature_op, 'loc': location,
                           'sts': status_op, 'day': day, 'src': src, 'dark': True}
            except:
                context = {'tmp': '', 'loc': 'No Location Found, Try entering your nearest place or city',
                'sts': '', 'day': '', 'src': '', 'title': 'Weather App', 'dark': True
                }
            return context
        city = request.POST['city']
        log(request, f'weather - {city}')
        return render(request, 'projects/weather.html', get_weather(city))
    log(request, 'weather')
    return render(request, 'projects/weather.html', context)
