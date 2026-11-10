from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("tasks.urls")),
    path("", lambda request: HttpResponse(
        "<h1>Task Manager</h1><p>API: <a href='/api/tasks/'>Список задач</a></p>"
        "<p><a href='/admin/'>Перейти в Django Admin</a></p>"
    )),
]
