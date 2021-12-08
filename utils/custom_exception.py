from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException


def custom_exception_handler(exc, context):
    error_class = exc.__class__.__name__

    response = exception_handler(exc, context)
    if response is not None:
        if error_class == 'ValidationError':
            response_obj = {}
            detail = exc.detail
            for key, value in detail.items():
                error_value = []
                for each_value in value:
                    error_value.append(each_value.title())
                response_obj[key] = error_value
            return Response(response_obj, status=400)

        else:
            response.data['status_code'] = response.status_code
            response.data['message'] = response.data['detail']
            del response.data['detail']

            return response



class InternalServerException(APIException):

    #public fields
    detail = None
    status_code = None

    # create constructor
    def __init__(self, status_code, message):
        #override public fields
        InternalServerException.status_code = status_code
        InternalServerException.detail = message