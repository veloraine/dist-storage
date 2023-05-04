from django.urls import path
from .views import file_request, save_file

urlpatterns = [
    path("file_request", file_request, name="file_request"),
    path("save_file", save_file, name="save_file"),
]
