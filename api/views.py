from django.http import HttpResponse
from base.models import AdminLog
from base.views import push
from django.shortcuts import render
# Create your views here.


def latest_log(request):
    context = {
        'title':'Latest Log',
        'dark': True,
        'content': AdminLog.objects.get(name='api_log').latest_log
    }
    return render(request, 'api/main.html',context)


def log(request):
    context = {
        'title': 'Jerit Baiju | Logs',
        'dark': True,
        'content': str(AdminLog.objects.get(name='api_log').log).split('\n'),
        'type': 'list'
    }
    return render(request, 'api/main.html', context)


def clr_admin_log(request):
    log = AdminLog.objects.get(name='api_log')
    log.log = ''
    log.save()
    push('API LOG CLEARED')
    return HttpResponse('Cleared')
