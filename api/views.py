from math import e
import os
from datetime import datetime

import pytz
import requests
from bs4 import BeautifulSoup
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

from base import basic
from base.models import AdminLog, AdminSecret, User

load_dotenv()
# Create your views here.

@csrf_exempt
def subscribe(request):
    if request.user.is_superuser:
        if request.method == "POST":
            try:
                token = request.POST.get('token')
                token_object = AdminSecret.objects.get(name='token')
                token_object.secret = token
                token_object.save()
            except:
                try:
                    token = request.POST.get('token')
                    token_object = AdminSecret.objects.create(name='token', secret=token)
                    token_object.save()
                except:
                    return JsonResponse({"status": "FAILED"})
        return render(request, 'api/subscribe.html', {'dark': True})
        


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


def logs(request):
    if request.user.is_superuser:
        context = {
            'title': 'Jerit Baiju | Logs',
            'dark': True,
            'content': str(AdminLog.objects.get(name='api_log').log).split('\n'),
            'type': 'list'
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


def weather(request, city):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }
    try:
        url = f"https://www.google.com/search?q=weather+in+{city}"
        page = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(page.content, 'html.parser')
        temperature = soup.find('span', attrs={'id': 'wob_ttm'}).text
        status = soup.find('span', attrs={'id': 'wob_dc'}).text
        # location = soup.find('div', attrs={'id': 'wob_loc'}).text
        location = city
        temperature_op = f"{temperature} °F \n"
        status_op = f"Status - {status} \n"
        image_url = soup.find('img', attrs={'id': 'wob_tci'}).get('src')
        time = soup.find('div', attrs={'id': 'wob_dts'}).text
        context = {'success': True, 'temp': temperature_op, 'location': location,
                   'status': status_op, 'time': time, 'image_url': image_url}
    except:
        context = {'success': False,
                   'op': 'No Location Found, Try entering your nearest place or city'}
    basic.log(request, f'Weather - {city}')
    return JsonResponse(context)


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
        stars = 6
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
