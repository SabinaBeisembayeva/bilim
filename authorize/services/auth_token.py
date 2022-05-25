from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication

from authorize.models import UserToken, User


class TokenAuthenticationCustom(TokenAuthentication):
    def __init__(self):
        super().__init__()

    model = UserToken

    def authenticate_credentials(self, key):
        model = self.get_model()
        tokens = model.objects.select_related('user').filter(key=key)
        if tokens.count() == 0:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))
        if not tokens[0].user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return (tokens[0].user, tokens)


def delete_token(user: User, token: str, all: bool):
    """Deletes an existing user token"""
    try:
        if all:
            UserToken.objects.filter(user=user).delete()
        else:
            UserToken.objects.get(user=user, key=token).delete()
    except UserToken.DoesNotExist:
        pass
