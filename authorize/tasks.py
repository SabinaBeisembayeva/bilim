import json
import requests
from django.core.mail import send_mail

from bilim.celery import app
from bilim.settings import EMAIL_USER_NAME
from authorize.models import User
# from Server.tasks import graylogging


@app.task(queue="high")
def sending_mail_to_user(title='Онлайн Касса', to=None, content=None):
    """Sending a letter to the user's email. If there is an error, send logs to graylog"""
    try:
        send_mail(
            title,
            'Bilim.co',
            EMAIL_USER_NAME,
            [to],
            fail_silently=False,
            html_message=content
        )
    except:
        pass
        # graylogging.apply_async((json.dumps(
        #     {
        #         'to': to,
        #         'short_message': 'Error when sending mail to User',
        #         'host': 'ukassa.kz',
        #         'content': content
        #     }), 'mail',))
