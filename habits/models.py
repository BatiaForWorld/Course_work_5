from django.conf import settings
from django.db import models


class Habit(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habits')
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='related_for',
    )
    periodicity = models.PositiveSmallIntegerField(default=1)
    reward = models.CharField(max_length=255, blank=True)
    execution_time = models.PositiveIntegerField(help_text='Время на выполнение в секундах')
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_reminder_sent_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.action} @ {self.time}'
