
import socket
import logging
import traceback
import threading

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
    

# Create a thread-local variable to store the current user
thread_local = threading.local()

def get_current_user():
    return getattr(thread_local, 'user', None)

# Middleware to set the current user for the thread
class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        thread_local.user = request.user
        response = self.get_response(request)
        return response

# Add 'path.to.CurrentUserMiddleware' to the MIDDLEWARE setting in settings.py