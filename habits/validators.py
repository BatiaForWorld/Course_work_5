from rest_framework.exceptions import ValidationError


def validate_reward_or_related(related_habit, reward):
    if related_habit and reward:
        raise ValidationError('Нельзя одновременно указывать связанную привычку и вознаграждение.')


def validate_execution_time(execution_time):
    if execution_time > 120:
        raise ValidationError('Время выполнения должно быть не больше 120 секунд.')


def validate_related_habit_is_pleasant(related_habit):
    if related_habit and not related_habit.is_pleasant:
        raise ValidationError('В связанные привычки можно добавлять только приятные привычки.')


def validate_pleasant_habit(is_pleasant, related_habit, reward):
    if is_pleasant and (related_habit or reward):
        raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки.')


def validate_periodicity(periodicity):
    if periodicity < 1 or periodicity > 7:
        raise ValidationError('Нельзя выполнять привычку реже, чем 1 раз в 7 дней.')


def validate_useful_habit_has_reward_or_related(is_pleasant, related_habit, reward):
    if not is_pleasant and not related_habit and not reward:
        raise ValidationError('Для полезной привычки нужно указать вознаграждение или связанную привычку.')
