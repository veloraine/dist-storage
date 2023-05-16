import base64
from io import BytesIO
import json

import requests
from storage.constants import NEIGHBOURS
from django.core.files.uploadedfile import InMemoryUploadedFile


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
    file_data = file.read()
    blob = BytesIO()
    blob.write(file_data)
    blob.seek(0)
    blob_base64 = base64.b64encode(blob.getvalue())
    blob_string = blob_base64.decode('utf-8')

    return blob_string


def blob_to_file(blob, file_name):
    blob_base64 = blob.encode('utf-8')
    blob_data = base64.b64decode(blob_base64)

    file = InMemoryUploadedFile(
        BytesIO(blob_data), None, file_name, None, len(blob_data), None)

    return file
