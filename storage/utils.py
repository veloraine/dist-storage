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


def convert_to_blob_bytes(file):
    return file.read()


def memoryview_to_file(memoryview, file_name):
    file_data = memoryview.tobytes()

    file = InMemoryUploadedFile(
        ContentFile(file_data), None, file_name, None, len(file_data), None)

    return file


def memoryview_to_blob_string(memory_view):
    blob_bytes = memory_view.tobytes()
    return base64.b64encode(blob_bytes).decode('utf-8')


def dict_to_log(dict_log):
    return Log(
        term=dict_log['term'],
        file_blob=base64.b64decode(dict_log['file_blob']),
        file_id=dict_log['file_id'],
        file_name=dict_log['file_name']
    )


def log_to_dict(log):
    return {
        'term': log.term,
        'file_blob': memoryview_to_blob_string(log.file_blob),
        'file_id': log.file_id,
        'file_name': log.file_name
    }
