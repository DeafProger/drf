from habits.validators import (PeriodicityValidator, RelatedHabitValidator,
                               DurationTimeValidator, RewardValidator)
from rest_framework import serializers
from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """Сериализотор модели привычки"""
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ['user']
        validators = [
            RewardValidator(field='reward'),
            RelatedHabitValidator(field='related_habit'),
            DurationTimeValidator(field='duration'),
            PeriodicityValidator(field='periodicity')
        ]
