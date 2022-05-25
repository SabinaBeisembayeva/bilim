import os
import random
from datetime import datetime
import binascii
from django.core.cache import cache
from django.db.models import Count
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.exceptions import ValidationError

from authorize.models import User, UserActivation, UserToken
from authorize.tasks import sending_mail_to_user




def send_renew_link_to_mail(user: User, email: str, code: None):
    if code is None:
        code = str(binascii.hexlify(os.urandom(15)).decode("utf-8"))
    sending_mail_to_user.apply_async(('Bilim.co - Forgot password?', email, code))
    # 20 minutes to change
    cache.set('code-{}'.format(code), email, 60 * 20)
    # 1 minutes to resend
    cache.set('email_time_' + str(email), email, 60)

def sending_activation_template_to_user(user: User):
    """The process of sending the activation template to the user's email!"""
    hash = hex(random.getrandbits(128))
    User.objects.create_activation(user, hash)
    content = None
    sending_mail_to_user.apply_async(('Bilim.co - User Activation', user.email, content))
