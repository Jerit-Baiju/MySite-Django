import datetime
import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from pytube import YouTube

from base.basic import log
from base.models import MediaFile, Video

# Create your views here.


def projects(request):
    log(request, 'Projects')
    projects_data = [
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
            'src': 'https://github.com/jerit-baiju/activity_generator', 'btn': 'GitHub'},
        {'name': 'YT video Downloader', 'info': 'You can download any youtube video with high resolution.',
            'src': reverse('yt_video'), 'btn': 'Download'}

    ]
    random.shuffle(projects_data)
    context = {
        'title': 'Projects | Jerit Baiju',
        'projects': projects_data,
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
def num_game(request):
    if request.user.score is None:
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
    log(request, 'Num Game')
    context = {
        'score': score,
        'title': 'Number Game',
        'randint': random.randint(0, 100),
        'dark': True
    }
    return render(request, 'projects/num_game.html', context)


@login_required(login_url='login-page')
def num_game_add(request):
    if request.user.is_authenticated:
        if request.user.score is None:
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

@login_required(login_url='login-page')
def yt_video(request):
    if request.method == 'POST':
        url = request.POST['yt_link']
        youtube = YouTube(url)
        video = youtube.streams.get_highest_resolution()
        if video.filesize_gb <= 3:
            path = video.download('media/', filename=f'{request.user.email}.mp4')
            time_to_delete = datetime.datetime.now() + datetime.timedelta(minutes=30)
            media_file = MediaFile.objects.create(file_path=path, time_to_delete=time_to_delete)
            media_file.save()
            vid = Video.objects.create(url=url, title=video.title, user=request.user)
            vid.save()
            log(request, f'YT_Video - {video.title} - {video.filesize_mb} GB')
            return FileResponse(open(f'media/{request.user.email}.mp4', 'rb'), as_attachment=True, filename=f'{video.title}.mp4')
        else:
            messages.info(request, f'So sorry {request.user.first_name}, your requested file is bigger than 3 GB of file size.')
            return render(request, 'projects/yt_video.html')

    else:
        return render(request, 'projects/yt_video.html')
