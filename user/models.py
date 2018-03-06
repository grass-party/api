from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from rest_framework import exceptions


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def social_auth(self, request, access_token, refresh_token, expires_in):
        user = authenticate(
            request=request, username=self.email, password='social')
        if not user:
            raise exceptions.AuthenticationFailed(
                'fail to django authenticate')

        login(request, user)

        request.session['access_token'] = access_token
        request.session['refresh_token'] = refresh_token
        request.session['expires_in'] = expires_in


class SocialAccount(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='socials',
                             on_delete=models.CASCADE)
    provider = models.CharField(max_length=10)
    account_id = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
