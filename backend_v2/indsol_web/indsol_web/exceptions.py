from rest_framework.views import exception_handler


from rest_framework.exceptions import APIException
from rest_framework import serializers, status


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None and response.status_code == 401:
        response.data["error"] = "Неверные данные для аутентификации"
    return response


class MediaValidationError(serializers.ValidationError):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Количество медиа файлов превышает допустимый лимит"
    default_code = "media_limit_error"


class ConflictError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Ошибка обновления сведений.'      
    default_code = 'conflict_error' 


class UnprocessableEntityError(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = 'Ошибка заполнения сведений.'      
    default_code = 'unprocessable_entity_error' 


class ForbiddenError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Доступ запрещен.'      
    default_code = 'unprocessable_entity_error' 
