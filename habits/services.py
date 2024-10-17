from datetime import datetime as dt
from django.utils import timezone
from django_celery_beat.models import (IntervalSchedule, PeriodicTask,
                                       CrontabSchedule)
from django_celery_beat.utils import make_aware
from config.settings import TELEGRAM_TOKEN
from habits.models import Habit
import requests
import json


def send_tg_message(message, chat_id):
    """    Отправка сообщения в Telegram    """
    params = {
        'text': message,
        'chat_id': chat_id
    }
    try:
        url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
        response = requests.get(url, params=params)
        response.raise_for_status()
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


def remind_of_habit(habit_id):
    """
    Напоминание о выполнении привычки
    """
    habit = Habit.objects.get(pk=habit_id)
    habtime = habit.time.strftime("%H:%M")
    message = f'''Привет!
Не забудь сегодня выполнить привычку: "{habit.action}" в {habtime}
Место: {habit.place}'''
    if habit.user.chat_id:
        send_tg_message(message, habit.user.chat_id)


def create_periodic_task(habit):
    """
    Создание периодической задачи Celery
    """
    start_time = (timezone.now().strftime("%d.%m.%Y") +
                  habit.time.strftime(" %H:%M:%S"))
    start_time_dt = dt.strptime(start_time, '%d.%m.%Y %H:%M:%S')
    aware_start_time_dt = make_aware(start_time_dt)

    def interval_sched(**kwargs):
        return IntervalSchedule.objects.get_or_create(**kwargs)

    def crontab_sched(**kwargs):
        return CrontabSchedule.objects.get_or_create(**kwargs)

    periodicity = {
        1: interval_sched(every=1, period=IntervalSchedule.DAYS),
        2: crontab_sched(minute=aware_start_time_dt.strftime("%M"),
                         hour=aware_start_time_dt.strftime("%H"),
                         day_of_week='1-5'),
        3: crontab_sched(minute=aware_start_time_dt.strftime("%M"),
                         hour=aware_start_time_dt.strftime("%H"),
                         day_of_week='6-7'),
        4: interval_sched(every=7, period=IntervalSchedule.DAYS),
    }

    period = periodicity[habit.periodicity][0]
    PeriodicTask.objects.create(
        interval=period if habit.periodicity in (1, 4) else None,
        crontab=period if habit.periodicity in (2, 3) else None,
        name=f'{habit.pk}',
        task='habits.tasks.habit_track',
        kwargs=json.dumps({'habit_id': habit.pk, }),
        start_time=aware_start_time_dt
    )
