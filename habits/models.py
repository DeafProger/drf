from django.core.validators import MaxValueValidator
from django.conf import settings
from datetime import timedelta
from django.db import models


class Habit(models.Model):
    PERIODICITY_CHOICES = [
        (1, 'Every day'),
        (2, 'Every work day'),
        (3, 'Every weekend'),
        (4, 'Every week')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user',
                             verbose_name='Пользователь')
    place = models.CharField(max_length=50, verbose_name='Место')
    time = models.TimeField(verbose_name='Время')
    action = models.CharField(max_length=300, verbose_name='Действие')
    is_nice = models.BooleanField(default=False, verbose_name='Признак приятной привычки')
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='main_habit',
                                      verbose_name='Связанная привычка')
    periodicity = models.PositiveIntegerField(default=1, choices=PERIODICITY_CHOICES, verbose_name='Периодичность')
    reward = models.CharField(max_length=300, blank=True, null=True, verbose_name='Вознаграждение')
    duration = models.DurationField(verbose_name='Длительность выполнения (сек)',
                                    validators=[MaxValueValidator(timedelta(seconds=120))])
    is_public = models.BooleanField(default=False, verbose_name='Признак публичности')

    def __str__(self):
        return f'Я буду {self.action} в {self.time} в {self.place}'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ('pk',)