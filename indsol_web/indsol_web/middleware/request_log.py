"""
Промежуточное логирование. Перехватывает request на момент 'перед' и 'после' запроса и передает в объект логгера
"""
import json
import logging
import os
import socket
import time

from querystring_parser import parser
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

request_logger = logging.getLogger(__name__)


class RequestLogMiddleware:
    """Request Logging Middleware."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        log_data = {
            "remote_address": request.META["REMOTE_ADDR"],
            "server_hostname": socket.gethostname(),
            "request_method": request.method,
            "request_path": request.get_full_path(),
        }

        # Обработка только "*/api/*" шаблонов
        if "/api/" in str(request.get_full_path()) and "form-data" in str(
            request.headers
        ):
            print("Логирование POST запросов")
            print(request.POST)
            req_body = parser.parse(request.POST.urlencode())
            log_data["request_body"] = req_body
        elif "/api/" in str(request.get_full_path()) and "application/json" in str(
            request.headers
        ):
            req_body = parser.parse(request.POST.urlencode()) if request.body else {}
            log_data["request_body"] = req_body

        # request передается обработчику
        response = self.get_response(request)

        request_logger.info(msg=log_data)

        return response

    # Обработка ошибок Django
    def process_exception(self, request, exception):
        log_data = {
            "remote_address": request.META["REMOTE_ADDR"],
            "server_hostname": socket.gethostname(),
            "request_method": request.method,
            "request_path": request.get_full_path(),
        }
        log_data["error_reason"] = f"{exception.__class__.__name__}"
        log_data["error_body"] = f"{exception}"

        request_logger.critical(msg=log_data)

        return None
