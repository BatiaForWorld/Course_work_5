from django.urls import path

from habits.views import HabitListCreateView, HabitRetrieveUpdateDestroyView, PublicHabitListView

urlpatterns = [
    path('', HabitListCreateView.as_view(), name='habit-list-create'),
    path('<int:pk>/', HabitRetrieveUpdateDestroyView.as_view(), name='habit-detail'),
    path('public/', PublicHabitListView.as_view(), name='public-habit-list'),
]
