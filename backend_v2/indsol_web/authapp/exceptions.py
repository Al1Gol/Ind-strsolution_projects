from rest_framework.exceptions import APIException
from rest_framework import status

class ConflictError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Ошибка обновления сведений.'      
    default_code = 'conflict_error' 


class UnprocessableEntityError(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = 'Ошибка заполнения сведений.'      
    default_code = 'unprocessable_entity_error' 