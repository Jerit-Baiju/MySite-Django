import random
from base.basic import log
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

# Create your views here.


def projects(request):
    log(request, 'Projects')
    projects = [
        {'name': 'Weather App', 'info': 'A project to get weather from all places, working by scrapping data from GOOGLE WEATHER.',
            'src': '/projects/weather', 'btn': 'Go'},
        {'name': 'PyFlit', 'info': 'Tool for adding components and pages in FLASK. Can be used to send PYTHON variables to JAVASCRIPT.',
            'src': 'https://pypi.org/project/pyflit/', 'btn': 'PYPI'},
        {'name': 'Clara', 'info': 'CHAT-BOT made with CHAT-BOT-API. Simple STATIC Project.',
            'src': '/projects/clara', 'btn': 'Chat'},
        {'name': 'MySite', 'info': 'DYNAMIC WEBSITE made with DJANGO framework, FEATURES - Admin Panel, User Management, User-Score Handling, LOGS, etc.. ',
            'src': 'https://github.com/jerit-baiju/mysite-django', 'btn': 'GitHub'},
        {'name': 'Number Game', 'info': 'You should assume the number that is picked from 0-100 randomly by computer with TEN chances.',
            'src': '/projects/num_game', 'btn': 'Play'},
        {'name': 'Chat Bot API', 'info': 'This API provides you free commands, wikipedia support, user detection.',
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


@login_required(login_url='login-page')
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
        messages.error(request, 'An unknown error occurred.')
        return redirect('num-game')


def weather(request):
    context = {
        'title': 'Weather App',
        'dark': True
    }
    return render(request, 'projects/weather.html', context)
