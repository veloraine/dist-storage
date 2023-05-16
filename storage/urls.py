from django.urls import path

from storage.views import broadcast_request, get_all_file, get_file, log_request, log_response, initialize, start_from_crash, vote_request, vote_response, get_variable

urlpatterns = [
    path("message/vote-request", vote_request, name="vote-request"),
    path("message/vote-response", vote_response, name="vote-response"),
    path("message/log-request", log_request, name="log-request"),
    path("message/log-response", log_response, name="log-response"),
    path("broadcast-request", broadcast_request, name="broadcast-request"),
    path("init", initialize, name="init"),
    path("restart", start_from_crash, name="restart"),
    path("var", get_variable, name="get_variable"),
    path("get-file", get_all_file, name="get_all_file"),
    path("get-file/<int:file_id>", get_file, name="get_file"),
]
