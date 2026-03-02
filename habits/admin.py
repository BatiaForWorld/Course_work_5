from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'action', 'time', 'is_pleasant', 'is_public')
    list_filter = ('is_pleasant', 'is_public', 'periodicity')
    search_fields = ('action', 'place', 'owner__username')
