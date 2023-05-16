import json
import pickle
from django.shortcuts import render
from rest_framework.decorators import api_view
from dist_storage.utils import response, validate_body, validate_params
from storage.raft import cancel_election_timer, on_receive_log_request, on_receive_log_response, on_receive_vote_request, on_receive_vote_response, request_to_broadcast, restart_election_timer
from storage.services import convert_to_blob, get_acked_length, get_all_neighbours_id, get_commit_length, get_current_leader, get_current_role, get_current_term, get_log, get_sent_length, get_vote_received, get_voted_for, init_persistent_variables, init_volatile_variables, is_file_id_exists, save_file
from .models import File
from .constants import *
from django.http import FileResponse
from django.core.cache import cache

# @api_view(['POST'])
# def file_request(request):
#     if request.method == 'POST':
#         is_valid = validate_body(request, ['file'])
#         if is_valid:
#             return is_valid

#         uploaded_file = request.FILES['file']

#         if uploaded_file.size > 1000000:
#             return response(data={'message': 'File size too large'}, status=400)

#         # TODO: change to check if leader with better mechanism
#         if IS_LEADER:
#             print("I'm Leader")
#             File.objects.create(uploaded_file=uploaded_file)
#             print(uploaded_file)

#             # TODO: write to log

#             # TODO: send to other nodes
#             for node in LIST_OF_NODES_URL:
#                 send_to_nodes(node + '/storage/save_file', [uploaded_file])

#             return response(data={'message': 'File uploaded successfully'})
#         else:
#             print("Not leader, forwarding to leader")
#             if res.status_from django.core.cache import cache
# code == 200:
#                 return response(data={'message': 'File uploaded successfully'})
#             return response(data={'message': 'File failed to upload'}, status=400)


@api_view(['POST'])
def broadcast_request(request):
    print("AAAAAAAAAA Got broadcast request")
    is_valid = validate_body(request, ['file'])
    if is_valid:
        return is_valid
    is_valid = validate_params(request, ['file_id'])
    if is_valid:
        return is_valid
    print("AAAAAAAAAA Validated")
    file_id = request.GET['file_id']
    if is_file_id_exists(file_id):
        return response(data={'message': 'File id already exists'}, status=400)

    file = request.FILES['file']
    print("AAAAAAAAAA Got file")
    request_to_broadcast(
        file_id=file_id,
        file=file
    )
    return response(data={'message': 'File uploaded successfully'})


@api_view(['GET'])
def get_all_file(request):
    files = File.objects.all()
    return response(data={'files': str(files)})


@api_view(['GET'])
def get_file(request, file_id):
    file_object = File.objects.get(id=file_id)
    return FileResponse(file_object.uploaded_file)


@api_view(['POST'])
def log_request(request):
    message = request.data
    on_receive_log_request(
        leader_id=message["leader_id"],
        term=message["current_term"],
        prefix_length=message["prefix_len"],
        prefix_term=message["prefix_term"],
        leader_commit=message["commit_length"],
        suffix=message["suffix"]
    )
    return response(data={'message': 'Log request received'})


@api_view(['POST'])
def log_response(request):
    message = request.data
    on_receive_log_response(
        follower=message["node_id"],
        term=message["current_term"],
        ack=message["ack"],
        success=message["flag"]
    )
    return response(data={'message': 'Log response received'})


@api_view(['POST'])
def vote_request(request):
    message = request.data
    on_receive_vote_request(
        c_id=message["candidate_id"],
        c_term=message["current_term"],
        c_log_length=message["log_length"],
        c_log_term=message["last_term"]
    )
    return response(data={'message': 'Vote request received'})


@api_view(['POST'])
def vote_response(request):
    message = request.data
    on_receive_vote_response(
        voter_id=message["voter_id"],
        vote_granted=message["vote_granted"],
        term=message["term"]
    )
    return response(data={'message': 'Vote response received'})


@api_view(['POST'])
def initialize(request):
    init_persistent_variables()
    init_volatile_variables()
    restart_election_timer()
    return response(data={'message': 'Node started successfully'})


@api_view(['POST'])
def start_from_crash(request):
    init_volatile_variables()
    restart_election_timer()
    return response(data={'message': 'Node restarted successfully'})


@api_view(['GET'])
def get_variable(request):
    data = {
        "current_role": str(get_current_role()),
        "current_leader": get_current_leader(),
        "current_term": get_current_term(),
        "voted_for": get_voted_for(),
        "vote_received": get_vote_received(),
        "log": get_log(),
        "sent_length": get_sent_length(),
        "acked_length": get_acked_length(),
        "commit_length": get_commit_length(),
        "neighbors": NEIGHBOURS,
    }
    return response(data=data)
