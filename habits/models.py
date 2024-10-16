from django.core.validators import MaxValueValidator
from django.conf import settings
from datetime import timedelta
from django.db import models


class Habit(models.Model):
    PERIODICITY_CHOICES = [(1, 'Every day'), (2, 'Every work day'),
                           (3, 'Every weekend'), (4, 'Every week')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Owner',
                             on_delete=models.CASCADE, related_name='user')
    place = models.CharField(max_length=50, verbose_name='Место')
    time = models.TimeField(verbose_name='Время')
    action = models.CharField(max_length=300, verbose_name='Действие')
    is_nice = models.BooleanField(verbose_name='Признак приятной привычки',
                                  default=False)
    related_habit = models.ForeignKey('self', blank=True, null=True,
                                      verbose_name='Связанная привычка',
                                      on_delete=models.SET_NULL,
                                      related_name='main_habit')
    periodicity = models.PositiveIntegerField(choices=PERIODICITY_CHOICES,
                                              verbose_name='Периодичность',
                                              default=1)
    reward = models.CharField(max_length=300, verbose_name='Вознаграждение',
                              blank=True, null=True)
    duration = models.DurationField(verbose_name='Длит-сть выполнения (сек)',
                                    validators=[MaxValueValidator(
                                        timedelta(seconds=120))])
    is_public = models.BooleanField(verbose_name='Признак публичности',
                                    default=False)

    def __str__(self):
        return f'Я буду {self.action} в {self.time} в {self.place}'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ('pk',)
