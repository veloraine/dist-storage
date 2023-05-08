from django.shortcuts import render
from rest_framework.decorators import api_view
from dist_storage.utils import response, validate_body, validate_params
from .models import File
from .constants import *
from django.http import FileResponse
import requests

@api_view(['POST'])
def file_request(request):
    if request.method == 'POST':
        is_valid = validate_body(request, ['file'])
        if is_valid:
            return is_valid
        
        uploaded_file = request.FILES['file']

        if uploaded_file.size > 1000000:
            return response(data={'message': 'File size too large'}, status=400)
        
        # TODO: change to check if leader with better mechanism
        if IS_LEADER:
            print("I'm Leader")
            File.objects.create(uploaded_file=uploaded_file)
            print(uploaded_file)

            # TODO: write to log

            # TODO: send to other nodes
            for node in LIST_OF_NODES_URL:
                send_to_nodes(node + '/storage/save_file', [uploaded_file])

            return response(data={'message': 'File uploaded successfully'})
        else:
            print("Not leader, forwarding to leader")
            res = requests.post(LEADER + '/storage/file_request', files={'file': uploaded_file})
            if res.status_code == 200:
                return response(data={'message': 'File uploaded successfully'})
            return response(data={'message': 'File failed to upload'}, status=400)

@api_view(['POST'])
def save_file(request):
    if request.method == 'POST':
        print("Incoming file from leader")
        is_valid = validate_body(request, ['file'])
        if is_valid:
            return is_valid
        
        uploaded_file = request.FILES['file']

        print(uploaded_file)
        File.objects.create(uploaded_file=uploaded_file)
        return response(data={'message': 'File uploaded successfully'})
    return response(data={'message': 'Something went wrong'}, status=400)

@api_view(['GET'])
def get_file(request):
    if request.method == 'GET':
        is_valid = validate_params(request, ['id'])
        if is_valid:
            return is_valid
        
        file_id = request.GET['id']
        file_object = File.objects.get(id=file_id)
        return FileResponse(file_object.uploaded_file)

def send_to_nodes(node_url, files):
    for i in files:
        print(f"Send to node: {node_url}")
        try:
            res = requests.post(node_url, files={'file': i})
            if res.status_code == 200:
                print(f"File sent successfully to {node_url}")
            else:
                print(f"File failed to send to {node_url}")
        except:
            print(f"File failed to send to {node_url}")


        

    
        
    
