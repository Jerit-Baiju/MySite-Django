from django.http import HttpResponse
from base.models import AdminLog
from base.views import push
# Create your views here.


def latest_log(request):
    context = AdminLog.objects.get(name='api_log').latest_log
    return HttpResponse(str(context))


def log(request):
    context = AdminLog.objects.get(name='api_log').log
    return HttpResponse(str(context).replace('\n','<br><br>'))


def clr_admin_log(request):
    log = AdminLog.objects.get(name='api_log')
    log.log = ''
    log.save()
    push('API LOG CLEARED')
    return HttpResponse('Cleared')
