from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def send_habit_reminders():
    now = timezone.localtime()
    current_time = now.time().replace(second=0, microsecond=0)

    habits = Habit.objects.select_related('owner').filter(time=current_time)
    for habit in habits:
        if not habit.owner.telegram_chat_id:
            continue

        if habit.last_reminder_sent_at:
            next_allowed = habit.last_reminder_sent_at + timedelta(days=habit.periodicity)
            if now < next_allowed:
                continue

        message = f'Напоминание: {habit.action}. Место: {habit.place}'
        if send_telegram_message(habit.owner.telegram_chat_id, message):
            habit.last_reminder_sent_at = now
            habit.save(update_fields=['last_reminder_sent_at'])
