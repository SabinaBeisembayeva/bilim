from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

import datetime
import os
import uuid
import binascii
from bilim import settings
from utils.consts import GENDER_CHOICES

class UserManager(BaseUserManager):
    """Manager for creating Super user and Simple user"""
    def create_user(self, email, name, phone, password=None):
        if not email or not name or not phone:
            raise ValueError('Users required fields [email, name, phone]')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone=phone
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, phone, password):
        user = self.create_user(
            email,
            name,
            phone,
            password=password
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)

        return user

    def create_activation(self, user, hash: str):
        return UserActivation.objects.create(
            user=user,
            code=hash
        )


class User(AbstractBaseUser):
    """Model of User, inherits from Django's AbstractBaseUser"""
    email = models.EmailField('eMail', unique=True, help_text='yourMail@bilim.kz')
    name = models.CharField('Name Surname', max_length=100, null=True)
    surname = models.CharField('Name Surname', max_length=100, null=True)
    phone = models.CharField('Mobile phone', unique=True, max_length=12, help_text='77071113377',
                             null=True)
    birthdate = models.DateField('Date of birth', null=True, blank=True)
    photo = models.ImageField('Photo', null=True, blank=True)
    created_at = models.DateTimeField('Date of registration', null=True, blank=True)
    is_active = models.BooleanField('Is active?', default=False)
    is_admin = models.BooleanField('Is admin?', default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

    def has_module_perms(self, arg):
        return True

    def has_perm(self, arg):
        return True

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class UserToken(models.Model):
    """The default authorization token model"""
    key = models.CharField(_("Key"), max_length=40, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='auth_tokens',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    user_agent = models.CharField(max_length=1000, null=True, blank=True)
    ip_address = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/encode/django-rest-framework/issues/705
        abstract = 'rest_framework.authtoken' not in settings.INSTALLED_APPS
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")
#13
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(UserToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key


class UserActivation(models.Model):
        """Model for user activation"""
        user = models.OneToOneField('authorize.User', on_delete=models.CASCADE,
                                    related_name='user_activation', verbose_name='User')
        code = models.CharField('Key', max_length=120, null=True)
        created_at = models.DateTimeField(auto_now_add=True)
        activated_at = models.DateTimeField(null=True, blank=True)

        def __str__(self):
            return "{} - {}".format(self.user, self.code)

        class Meta:
            verbose_name = 'Activation'
            verbose_name_plural = 'Activation'


class Profile(models.Model):
    user = models.OneToOneField('authorize.User', on_delete=models.CASCADE,
                                    related_name='user_profile', verbose_name='User')
    # gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    school = models.OneToOneField('school.School', on_delete=models.CASCADE,
                                    related_name='school_profile', verbose_name='School')
                                    