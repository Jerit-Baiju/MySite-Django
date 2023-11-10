from datetime import datetime

import firebase_admin
import pytz
from django.http import JsonResponse
from firebase_admin import credentials, messaging

from base.models import AdminLog, AdminSecret

cred = credentials.Certificate('firebase.json')
firebase_admin.initialize_app(cred)


def push(text):
    try:
        token = AdminSecret.objects.get(name="token").secret
        message = messaging.Message(notification=messaging.Notification(
            title='Jerit Baiju', body=text), token=token, data={'icon': 'https://jerit.in/static/favicon.png'})
        response = messaging.send(message)
        return JsonResponse({'status': response})
    except:
        return JsonResponse({'status': 'push failed'})


def log(request, data):
    date = datetime.now(pytz.timezone("Asia/Kolkata")
                        ).date().strftime(r"%b %d, %Y")
    time = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%I:%M %p")
    agent = request.META['HTTP_USER_AGENT']
    admin_log, _ = AdminLog.objects.get_or_create(name='api_log')
    if request.user.is_authenticated:
        if not request.user.is_superuser:
            user = request.user
            body = f"{date} | {time} | {user} | {data} | {agent}"
            admin_log.latest_log = body
            admin_log.log = f"{body}\n{admin_log.log}"
            admin_log.save()
            user_log = f"{date} | {time} | {data} | {agent}\n{user.log}"
            user.log = user_log
            user.save()
    else:
        body = f"{date} | {time} | {data} | {agent}"
        admin_log.latest_log = body
        admin_log.log = f"{body}\n{admin_log.log}"
        admin_log.save()
