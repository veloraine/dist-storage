from django.urls import path

from storage.views import broadcast_request, get_all_file, get_file, log_request, log_response, initialize, start_from_crash, upload_file, vote_request, vote_response, get_variable

urlpatterns = [
    path("message/vote-request", vote_request, name="vote-request"),
    path("message/vote-response", vote_response, name="vote-response"),
    path("message/log-request", log_request, name="log-request"),
    path("message/log-response", log_response, name="log-response"),
    path("message/broadcast-request", broadcast_request, name="broadcast-request"),
    path("upload-file", upload_file, name="upload-file"),
    path("init", initialize, name="init"),
    path("restart", start_from_crash, name="restart"),
    path("var", get_variable, name="get-variable"),
    path("get-file", get_all_file, name="get-all-file"),
    path("get-file/<int:file_id>", get_file, name="get-file"),
]
