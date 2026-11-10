from django.db.models import Count
from django.utils import timezone
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Task, SubTask
from .serializers import (
    TaskCreateSerializer,
    TaskDetailSerializer,
    SubTaskSerializer,
    SubTaskCreateSerializer,
)


# Переводим название дня недели в формат Django:
# Sunday = 1, Monday = 2, ..., Saturday = 7.
WEEKDAYS = {
    "monday": 2,
    "понедельник": 2,
    "tuesday": 3,
    "вторник": 3,
    "wednesday": 4,
    "среда": 4,
    "thursday": 5,
    "четверг": 5,
    "friday": 6,
    "пятница": 6,
    "saturday": 7,
    "суббота": 7,
    "sunday": 1,
    "воскресенье": 1,
}


class TaskListCreateAPIView(generics.ListCreateAPIView):
    # GET — список задач, POST — создание новой задачи.
    queryset = Task.objects.all()

    def get_queryset(self):
        tasks = Task.objects.all()

        # Если параметр weekday не передан, показываем все задачи.
        # Можно передать название дня на русском или английском языке.
        weekday = self.request.query_params.get("weekday")

        if weekday:
            weekday = weekday.strip().lower()
            day_number = WEEKDAYS.get(weekday)

            if day_number is None:
                return Task.objects.none()

            # Фильтруем задачи по дню недели в поле deadline.
            tasks = tasks.filter(deadline__week_day=day_number)

        return tasks.order_by("-created_at")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TaskCreateSerializer
        return TaskDetailSerializer


class TaskDetailAPIView(generics.RetrieveAPIView):
    # GET — получение одной задачи по её ID.
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer


class TaskStatisticsAPIView(APIView):
    # GET — статистика по задачам.
    def get(self, request):
        total_tasks = Task.objects.count()

        tasks_by_status = Task.objects.values("status").annotate(
            total=Count("id")
        )

        status_statistics = {}
        for item in tasks_by_status:
            status_statistics[item["status"]] = item["total"]

        overdue_tasks = Task.objects.filter(
            deadline__lt=timezone.now()
        ).exclude(status="Done").count()

        return Response({
            "total_tasks": total_tasks,
            "tasks_by_status": status_statistics,
            "overdue_tasks": overdue_tasks,
        })


class SubTaskPagination(PageNumberPagination):
    # На одной странице показываем максимум 5 подзадач.
    page_size = 5


class SubTaskListCreateView(generics.ListCreateAPIView):
    # GET — список подзадач, POST — создание подзадачи.
    # Сначала показываем последние добавленные подзадачи.
    queryset = SubTask.objects.all().order_by("-created_at")
    serializer_class = SubTaskCreateSerializer
    pagination_class = SubTaskPagination

    def get_queryset(self):
        subtasks = SubTask.objects.select_related("task").all()

        # Фильтр по названию главной задачи.
        task_title = self.request.query_params.get("task_title")
        if task_title:
            subtasks = subtasks.filter(task__title__icontains=task_title)

        # Фильтр по статусу подзадачи.
        status = self.request.query_params.get("status")
        if status:
            subtasks = subtasks.filter(status__iexact=status)

        # Последние созданные подзадачи идут первыми.
        return subtasks.order_by("-created_at")


class SubTaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # GET — одна подзадача, PUT/PATCH — обновление, DELETE — удаление.
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
