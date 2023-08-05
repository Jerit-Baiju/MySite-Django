import os
from datetime import datetime

import pytz
import requests
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

from base import basic
from base.models import AdminLog, AdminSecret

load_dotenv()
# Create your views here.

quotes = [
    '"Happiness is not something ready-made. It comes from your own actions." - Dalai Lama',
    '"The purpose of our lives is to be happy." - Dalai Lama',
    '"Happiness is a direction, not a place." - Sydney J. Harris',
    '"The best way to cheer yourself is to try to cheer someone else up." - Mark Twain',
    '"Happiness is when what you think, what you say, and what you do are in harmony." - Mahatma Gandhi',
    '"The only thing that will make you happy is being happy with who you are." - Goldie Hawn',
    '"Happiness is not a goal; it\'s a by-product." - Eleanor Roosevelt',
    '"The secret of happiness is not in doing what one likes, but in liking what one does." - James M. Barrie',
    '"Success is not the key to happiness. Happiness is the key to success. If you love what you are doing, you will be successful." - Albert Schweitzer',
    '"Happiness is letting go of what you think your life is supposed to look like and celebrating it for everything that it is." - Mandy Hale',
    '"Be happy with what you have. Be excited about what you want." - Alan Cohen',
    '"The most important thing is to enjoy your life - to be happy - its all that matters." - Audrey Hepburn',
    '"The only joy in the world is to begin." - Cesare Pavese',
    '"Happiness is not in the mere possession of money; it lies in the joy of achievement, in the thrill of creative effort." - Franklin D. Roosevelt',
    '"Be happy for this moment. This moment is your life." - Omar Khayyam'
]


@csrf_exempt
def subscribe(request):
    if request.user.is_superuser:
        if request.method == "POST":
            try:
                token = request.POST.get('token')
                token_object = AdminSecret.objects.get(name='token')
                token_object.secret = token
                token_object.save()
                return JsonResponse({"status": "UPDATED SUCCESSFULLY"})
            except:
                try:
                    token = request.POST.get('token')
                    token_object = AdminSecret.objects.create(
                        name='token', secret=token)
                    token_object.save()
                    return JsonResponse({"status": "CREATED SUCCESSFULLY"})
                except:
                    return JsonResponse({"status": "FAILED"})
        return render(request, 'api/subscribe.html', {'dark': True, 'firebase_key': os.environ['firebase']})
    return JsonResponse({"status": "Access Denied"})


def latest_log(request):
    email = request.GET.get('email')
    password = request.GET.get('pass')
    if email == 'jeritalumkal@gmail.com':
        user = authenticate(request, email=email, password=password)
    else:
        user = None
    if user is not None:
        context = {
            'title': 'Latest Log',
            'dark': True,
            'content': AdminLog.objects.get(name='api_log').latest_log
        }
        return render(request, 'api/main.html', context)
    else:
        context = {
            'title': 'Latest Log',
            'dark': True,
            'content': 'Access Denied'
        }
        return render(request, 'api/main.html', context)


def logs(request, page):
    if request.user.is_superuser:
        page = max(page, 1)
        all_logs = str(AdminLog.objects.get(name='api_log').log).split('\n')
        # Split logs into pages with 20 logs per page
        paginator = Paginator(all_logs, 20)
        # Get the logs for the requested page
        page_obj = paginator.get_page(page)
        context = {
            'title': 'Jerit Baiju | Logs',
            'dark': True,
            'content': page_obj,  # Pass the logs for the requested page to the template
            'type': 'list',
            'page': page,
            'next': page + 1,
            'previous': max(page - 1, 1)
        }
        return render(request, 'api/main.html', context)
    context = {
        'title': 'Latest Log',
        'dark': True,
        'content': 'Access Denied'
    }
    return render(request, 'api/main.html', context)


def clr_admin_log(request):
    email = request.GET.get('email')
    password = request.GET.get('pass')
    if email == 'jeritalumkal@gmail.com':
        user = authenticate(request, email=email, password=password)
    else:
        user = None
    if user is not None:
        api_log = AdminLog.objects.get(name='api_log')
        api_log.log = ''
        api_log.save()
        basic.push('API LOG CLEARED')
        context = {
            'title': 'Latest Log',
            'dark': True,
            'content': 'Cleared'
        }
        return render(request, 'api/main.html', context)
    context = {
        'title': 'Latest Log',
        'dark': True,
        'content': 'Access Denied'
    }
    return render(request, 'api/main.html', context)


def github_api(request):
    basic.log(request, 'github-api-fetch')
    auth = ('jerit-baiju', os.environ['github_api'])
    try:
        update_url = 'https://api.github.com/repos/jerit-baiju/mysite-django'
        github_url = "https://api.github.com/users/jerit-baiju"
        star_url = "https://api.github.com/repos/Jerit-Baiju/MySite-Django/stargazers"
        repos_url = "https://api.github.com/users/jerit-baiju/repos"
        updated_at = requests.get(update_url, auth=auth, timeout=10).json()[
            'pushed_at']
        github = requests.get(github_url, auth=auth, timeout=10).json()
        repos = requests.get(repos_url, auth=auth, timeout=10).json()
        stars = 2
        for repo in repos:
            stars += repo["stargazers_count"]
        update_date = datetime.strptime(updated_at, r"%Y-%m-%dT%H:%S:%fZ")
        update = update_date.astimezone(pytz.timezone(
            "Asia/Kolkata")).strftime(r"%B %d, %Y")
        stars_this = len(requests.get(star_url, auth=auth, timeout=10).json())
        repositories = github['public_repos']
        followers = github['followers']
        following = github['following']
        data = {'updated_at': update, 'stars_this': stars_this, 'repositories': repositories,
                'followers': followers, 'following': following, 'stars': stars}
        cache.set('github_data', data, timeout=24*60*60)
        return data
    except:
        data = cache.get('github_data')
        if data is None:
            data = {'updated_at': 'update', 'stars_this': 'stars_this', 'repositories': 'repositories',
                    'followers': 'followers', 'following': 'following', 'stars': 'stars'}
        return data
