from base.models import AdminLog
from base.views import push, log
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
# Create your views here.


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
    email = request.GET.get('email')
    password = request.GET.get('pass')
    if email == "jeritalumkal@gmail.com":
        user = authenticate(request, email=email, password=password)
    else:
        user = None
    if user is not None:
        context = {
            'title': 'Jerit Baiju | Logs',
            'dark': True,
            'content': str(AdminLog.objects.get(name='api_log').log).split('\n'),
            'type': 'list'
        }
        return render(request, 'api/main.html', context)
    else:
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
        log = AdminLog.objects.get(name='api_log')
        log.log = ''
        log.save()
        push('API LOG CLEARED')
        context = {
            'title': 'Latest Log',
            'dark': True,
            'content': 'Cleared'
        }
        return render(request, 'api/main.html', context)
    else:
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
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        temperature = soup.find('span', attrs={'id': 'wob_ttm'}).text
        status = soup.find('span', attrs={'id': 'wob_dc'}).text
        location = soup.find('div', attrs={'id': 'wob_loc'}).text
        temperature_op = (f"{temperature} °F \n")
        status_op = (f"Status - {status} \n")
        image_url = soup.find('img', attrs={'id': 'wob_tci'}).get('src')
        time = soup.find('div', attrs={'id': 'wob_dts'}).text
        context = {'success': True, 'temp': temperature_op, 'location': location,
                   'status': status_op, 'time': time, 'image_url': image_url}
    except:
        context = {'success': False,
                   'op': 'No Location Found, Try entering your nearest place or city'}
    log(request, f'weather - {city}')
    return JsonResponse(context)
