from base.models import AdminLog
from base.views import push
from base.views import log as add_log
from django.shortcuts import render
from django.contrib.auth import authenticate
# Create your views here.


def latest_log(request):
    username = request.GET.get('user')
    password = request.GET.get('pass')
    if username == 'jerit':
        user = authenticate(request, username=username, password=password)
    else:
        user = None
    if user is not None:
        context = {
            'title': 'Latest Log',
            'dark': True,
            'content': AdminLog.objects.get(name='api_log').latest_log
        }
        if username != 'jerit':
            add_log(request, 'Accessed Latest Log')
        return render(request, 'api/main.html', context)
    else:
        context = {
            'title': 'Latest Log',
            'dark': True,
            'content': 'Auth Failed'
        }
        return render(request, 'api/main.html', context)


def log(request):
    username = request.GET.get('user')
    password = request.GET.get('pass')
    if username in ['jerit', 'appuaa']:
        user = authenticate(request, username=username, password=password)
    else:
        user = None
    if user is not None:
        context = {
            'title': 'Jerit Baiju | Logs',
            'dark': True,
            'content': str(AdminLog.objects.get(name='api_log').log).split('\n'),
            'type': 'list'
        }
        if username != 'jerit':
            add_log(request, 'Accessed Logs')
        return render(request, 'api/main.html', context)
    else:
        context = {
            'title': 'Latest Log',
            'dark': True,
            'content': 'Auth Failed'
        }
        return render(request, 'api/main.html', context)


def clr_admin_log(request):
    username = request.GET.get('user')
    password = request.GET.get('pass')
    if username == 'jerit':
        user = authenticate(request, username=username, password=password)
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
            'content': 'Auth Failed'
        }
        return render(request, 'api/main.html', context)
