from django.db.models import Count
from django.utils import timezone
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Task, SubTask
from .serializers import (
    TaskCreateSerializer,
    TaskDetailSerializer,
    SubTaskSerializer,
    SubTaskCreateSerializer,
)


class TaskListCreateAPIView(generics.ListCreateAPIView):
    # GET — список задач, POST — создание новой задачи.
    queryset = Task.objects.all()

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


class SubTaskListCreateView(generics.ListCreateAPIView):
    # GET — список всех подзадач, POST — создание подзадачи.
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer


class SubTaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # GET — одна подзадача, PUT/PATCH — обновление, DELETE — удаление.
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
