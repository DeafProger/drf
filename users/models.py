from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    """Модель пользователя, авторизация по email"""
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    tg_id = models.CharField(max_length=30, verbose_name='ТелеграмID',
                             blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
