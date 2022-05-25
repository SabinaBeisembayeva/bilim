from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.exceptions import ValidationError
from django.utils import timezone

from authorize.models import UserToken, User, UserActivation


def authenticate_user(email, password, ip, user_agent):
    """Authorize user. If ok, creates a new token or gets the old one and
     returns the user object. If wrong, it returns an error"""
    data = {
        'username': email,
        'password': password
    }
    serializer = AuthTokenSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    user = serializer.validated_data.get('user')
    UserToken.objects.create(user=user, ip_address=ip, user_agent=user_agent)

    return user

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def user_email_existence(email: str):
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        raise ValidationError({'status': 1, 'detail': 'User not found'})

def activate_user(code: str):
    try:
        activation = UserActivation.objects.get(code=code, user__is_active=False)
    except UserActivation.DoesNotExist:
        raise ValidationError({
            'status': 0, 'detail': 'Code not found'
        })
    except:
        pass
    user = activation.user
    user.is_active = True
    user.save()

    activation.activated_at = timezone.localtime()
    activation.save()
