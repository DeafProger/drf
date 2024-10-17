from habits.services import remind_of_habit
from celery import shared_task


@shared_task
def habit_track(habit_id):
    """
        Задача Celery для напоминания о выполнении привычки
    """
    remind_of_habit(habit_id)
