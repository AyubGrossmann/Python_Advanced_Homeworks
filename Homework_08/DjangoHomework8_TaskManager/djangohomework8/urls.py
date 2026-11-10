from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", lambda request: HttpResponse(
        "<h1>Task Manager</h1><p>Домашнее задание 8. "
        '<a href="/admin/">Перейти в Django Admin</a></p>'
    )),
]
