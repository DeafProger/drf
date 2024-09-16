from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    phone = models.CharField(max_length=15, verbose_name='Телефон', blank=True, null=True)
    city = models.CharField(max_length=35, verbose_name='Город', blank=True, null=True)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email