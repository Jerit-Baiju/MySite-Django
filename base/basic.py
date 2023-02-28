import os
from datetime import datetime

import pytz
from pyfcm import FCMNotification

from .models import AdminLog, Device, User

fcm_api = os.environ['fcm_api_key']
fcm = FCMNotification(api_key=fcm_api)


def push(text):
    try:
        data = {
            'body': text,
        }
        super_user = User.objects.filter(is_superuser=True).first()
        device = Device.objects.filter(user_id=super_user).first()
        token = device.token
        message = fcm.notify_single_device(registration_id=token, data=data)
        return message
    except:
        pass


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
