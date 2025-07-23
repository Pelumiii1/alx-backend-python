from datetime import datetime
import logging

logger = logging.getLogger('request_logger')
if not logger.hasHandlers():
    handler = logging.FileHandler('requests.log')
    formatter = logging.Formatter('%(message)s')
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_reponse = get_response
        
    def __call__(self,request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()}- User:{user} - Path:{request.path}"
        logging.info(log_message)
        
        response = self.get_reponse(request)
        return response