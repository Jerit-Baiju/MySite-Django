from datetime import datetime

import pytz
from django.http import JsonResponse
from firebase_admin import messaging

from base.models import AdminLog, PWASubscription, User


def push(text):
    admin_users = User.objects.filter(is_superuser=True)
    for user in admin_users:
        try:
            pwa_subscription = PWASubscription.objects.get(user=user)
            registration_id = pwa_subscription.subscription.get('endpoint', '')
            if registration_id:
                message = messaging.Message(notification=messaging.Notification(title='Jerit Baiju', body=text), token=subcription.registration_token)
                response = messaging.send(message)
                print('Successfully sent message:', response)
        except PWASubscription.DoesNotExist:
            pass
    return JsonResponse({'status': 'ok'})


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
