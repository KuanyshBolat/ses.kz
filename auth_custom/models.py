from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    INVESTOR = 1
    COMPANY = 2
    NONE = 3

    ROLE_CHOICES = (
        (INVESTOR, 'Инвестор'),
        (COMPANY, 'Компания'),
        (NONE, 'Никто')
    )
    role = models.IntegerField(choices=ROLE_CHOICES, default=NONE)

    full_name = models.CharField(max_length=60)
    email = models.EmailField(_('email address'))
    phone = models.CharField(max_length=17)

    def __str__(self):
        return f'<User: full_name: {self.full_name}>'

    @property
    def company(self):
        return self._company.first()