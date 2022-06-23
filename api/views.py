from django.http import HttpResponse
from base.models import AdminLog
from base.views import push
from django.shortcuts import render
from django.contrib.auth import authenticate
# Create your views here.


def latest_log(request):
    username = request.GET.get('user')
    password = request.GET.get('pass')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        context = {
            'title':'Latest Log',
            'dark': True,
            'content': AdminLog.objects.get(name='api_log').latest_log
        }
        return render(request, 'api/main.html',context)
    else:
        return HttpResponse('UNKNOWN USER')


def log(request):
    username = request.GET.get('user')
    password = request.GET.get('pass')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        context = {
            'title': 'Jerit Baiju | Logs',
            'dark': True,
            'content': str(AdminLog.objects.get(name='api_log').log).split('\n'),
            'type': 'list'
        }
        return render(request, 'api/main.html', context)
    else:
        return HttpResponse('UNKNOWN USER')


def clr_admin_log(request):
    username = request.GET.get('user')
    password = request.GET.get('pass')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        log = AdminLog.objects.get(name='api_log')
        log.log = ''
        log.save()
        push('API LOG CLEARED')
        return HttpResponse('Cleared')
    else:
        return HttpResponse('UNKNOWN USER')
