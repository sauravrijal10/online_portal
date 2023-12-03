# # myapp/middleware.py

# import logging

# class RequestLogMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Log API endpoint information
#         self.log_api_request(request)

#         response = self.get_response(request)
#         return response

#     def log_api_request(self, request):
#         # Customize this log format based on your requirements
#         log_message = f"Method: {request.method}, Path: {request.path}, IP: {request.META.get('REMOTE_ADDR')}"

#         # Log the message to the 'api_log' logger
#         logger = logging.getLogger('api_log')
#         logger.info(log_message)
import socket
import logging
import traceback
logger = logging.getLogger('user.views')

class RequestLogMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_body = request.body,
        response = self.get_response(request)

        log_data = {
            "endpoint": request.META.get("HTTP_REFERER", ""),
            "remote_address": request.META["REMOTE_ADDR"],
            "server_hostname": socket.gethostname(),
            "request_method": request.method,
            "request_path": request.get_full_path(),
            "trace_back" : traceback.format_exc(),
            "status_code" : str(getattr(response, 'status_code', '')),
            "req_header" : request.headers,
            "body" : request_body, 
        }

        logger.warning(msg=log_data)

        return response