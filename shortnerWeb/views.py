from django.shortcuts import render
from django.http import HttpRequest
import logging

logger = logging.getLogger(__name__)


# Create your views here.
def main_page(request: HttpRequest):
    """Main page view for the URL shortener"""

    response = render(request, 'shortner/main.html')
    logger.debug(f'{request.method} {request.scheme}://{request.get_host()}{request.path} {response.status_code}')
    return response
