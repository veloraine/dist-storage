import base64
from io import BytesIO
import json

import requests
from storage.constants import NEIGHBOURS
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from storage.models import Log


def send_to_node(target_id, endpoint, payload):
    print("Sending to", target_id, endpoint)
    print(payload.to_dict())
    target = None
    for neighbour in NEIGHBOURS:
        if (neighbour["id"] == target_id):
            target = neighbour
            break
    if (target == None):
        print(f"FAILED TO SEND TO: {target_id}, id not found")
        return

    url = neighbour["url"] + endpoint
    headers = {
        'Content-Type': 'application/json'
    }
    data = json.dumps(payload.to_dict())
    try:
        requests.request("POST", url, headers=headers, data=data)
    except requests.exceptions.ConnectionError:
        print(f"CONNECTION ERROR: {url}, {data}")


def broadcast(endpoint, payload):
    print("Broadcasting", endpoint)
    print(payload.to_dict())
    for neighbour in NEIGHBOURS:
        url = neighbour["url"] + endpoint
        headers = {
            'Content-Type': 'application/json'
        }
        data = json.dumps(payload.to_dict())
        try:
            requests.request("POST", url, headers=headers, data=data)
        except requests.exceptions.ConnectionError:
            print(f"CONNECTION ERROR: {url}, {data}")


def convert_to_blob(file):
    blob_base64 = base64.b64encode(file.read())
    blob_string = blob_base64.decode('utf-8')

    return blob_string


def memoryview_to_file(memoryview, file_name):
    file_data = memoryview.tobytes()

    file = InMemoryUploadedFile(
        ContentFile(file_data), None, file_name, None, len(file_data), None)

    return file


def list_of_dict_to_log(list_of_dict):
    list_of_model = []
    for d in list_of_dict:
        list_of_model.append(Log(**d))
    return list_of_model
