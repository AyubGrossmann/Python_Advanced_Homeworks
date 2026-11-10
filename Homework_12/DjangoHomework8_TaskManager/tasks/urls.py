from django.urls import path
from .views import (
    TaskListCreateAPIView,
    TaskDetailAPIView,
    TaskStatisticsAPIView,
)

urlpatterns = [
    path("tasks/", TaskListCreateAPIView.as_view(), name="task-list-create"),
    path("tasks/<int:pk>/", TaskDetailAPIView.as_view(), name="task-detail"),
    path("tasks/statistics/", TaskStatisticsAPIView.as_view(), name="task-statistics"),
]
