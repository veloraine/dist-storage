from rest_framework import status
from rest_framework.response import Response

def validate_params(request, params):
    for param in params:
        res = request.query_params.get(param)
        if res is None:
            return response(error=f"{param} is required", status=status.HTTP_404_NOT_FOUND)
    return None
	
def validate_body(request, attrs):
    for attr in attrs:
        res = request.data.get(attr)
        if res is None:
            return response(error=f"{attr} is required", status=status.HTTP_404_NOT_FOUND)
    return None

def response(status = status.HTTP_200_OK, data = None, error = None):
    return Response({
					"data": data,
					"error": error,
				}, status=status)