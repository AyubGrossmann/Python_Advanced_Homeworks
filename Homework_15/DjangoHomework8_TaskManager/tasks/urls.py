from django.urls import path

from .views import (
    TaskListCreateAPIView,
    TaskRetrieveUpdateDestroyAPIView,
    TaskStatisticsAPIView,
    SubTaskListCreateView,
    SubTaskRetrieveUpdateDestroyView,
)

urlpatterns = [
    # Маршруты для задач.
    path("tasks/", TaskListCreateAPIView.as_view(), name="task-list-create"),
    path("tasks/statistics/", TaskStatisticsAPIView.as_view(), name="task-statistics"),
    path(
        "tasks/<int:pk>/",
        TaskRetrieveUpdateDestroyAPIView.as_view(),
        name="task-detail",
    ),

    # Маршруты для подзадач.
    path("subtasks/", SubTaskListCreateView.as_view(), name="subtask-list-create"),
    path(
        "subtasks/<int:pk>/",
        SubTaskRetrieveUpdateDestroyView.as_view(),
        name="subtask-detail",
    ),
]
