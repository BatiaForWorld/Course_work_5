from rest_framework import serializers

from habits.models import Habit
from habits.validators import (
    validate_execution_time,
    validate_periodicity,
    validate_pleasant_habit,
    validate_related_habit_is_pleasant,
    validate_reward_or_related,
    validate_useful_habit_has_reward_or_related,
)


class HabitSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Habit
        fields = (
            'id',
            'owner',
            'place',
            'time',
            'action',
            'is_pleasant',
            'related_habit',
            'periodicity',
            'reward',
            'execution_time',
            'is_public',
            'created_at',
        )
        read_only_fields = ('id', 'created_at')

    def validate(self, attrs):
        related_habit = attrs.get('related_habit', getattr(self.instance, 'related_habit', None))
        reward = attrs.get('reward', getattr(self.instance, 'reward', ''))
        execution_time = attrs.get('execution_time', getattr(self.instance, 'execution_time', 0))
        periodicity = attrs.get('periodicity', getattr(self.instance, 'periodicity', 1))
        is_pleasant = attrs.get('is_pleasant', getattr(self.instance, 'is_pleasant', False))

        validate_reward_or_related(related_habit, reward)
        validate_execution_time(execution_time)
        validate_related_habit_is_pleasant(related_habit)
        validate_pleasant_habit(is_pleasant, related_habit, reward)
        validate_periodicity(periodicity)
        validate_useful_habit_has_reward_or_related(is_pleasant, related_habit, reward)

        return attrs
