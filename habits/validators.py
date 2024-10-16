from rest_framework.serializers import ValidationError
from rest_framework import serializers


class RewardValidator:
    """
    Валидатор поля reward.
    Проверяет условия:
    - У приятной привычки не может быть вознаграждения.
    - В модели не должно быть заполнено одновременно и поле вознаграждения,
      и поле связанной привычки.
    Можно заполнить только одно из двух полей.
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reward = value.get(self.field)
        related_habit = value.get('related_habit')
        is_nice = value.get('is_nice')
        if reward and is_nice:
            raise serializers.ValidationError(
                'У приятной привычки не может быть вознаграждения')
        elif reward and related_habit:
            raise serializers.ValidationError(
                'В модели не должно быть заполнено одновременно и поле' +
                ' вознаграждения, и поле связанной привычки.')


class RelatedHabitValidator:
    """
    Валидатор поля related_habit.
    Проверяет условия:
    - В связанные привычки могут попадать только привычки с признаком
      приятной привычки.
    - У приятной привычки не может быть связанной привычки.
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        related_habit = value.get(self.field)
        is_nice = value.get('is_nice')
        if related_habit and not related_habit.is_nice:
            raise serializers.ValidationError(
                'В связанные привычки могут попадать только привычки с' +
                ' признаком приятной привычки.')
        if related_habit and is_nice:
            raise serializers.ValidationError(
                'У приятной привычки не может быть связанной привычки.')


class DurationTimeValidator:
    """Проверка продолжительности выполнения привычки: не более 2 минут"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        period_time = dict(value).get(self.field)
        if period_time and int(period_time) >= 120:
            raise ValidationError(
                "Время выполнения привычки должно быть не больше 120 секунд."
            )


class PeriodicityValidator:
    """Проверка периодичности выполнения привычки не реже,
    чем 1 раз в 7 дней"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        periodicity = dict(value).get(self.field)
        if periodicity:
            if not 1 <= int(periodicity) <= 7:
                raise ValidationError(
                    "Нельзя выполнять привычку реже, чем 1 раз в 7 дней"
                )
