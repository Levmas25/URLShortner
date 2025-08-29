import logging
import time

from django.shortcuts import redirect
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpRequest
from rest_framework import status
from django.utils.timezone import datetime

from .models import ShortedURL
from .serializers import ShortedURLSerializer


logger = logging.getLogger(__name__)


# Create your views here.
class URLShortnerAPIView(CreateAPIView):
    """
        Creates shorted url via api
    """
    serializer_class = ShortedURLSerializer
    queryset = ShortedURL.objects.all()
    

    def post(self, request: HttpRequest, *args, **kwargs):
        logger.debug(f'{request.method} {request.path} with body {request.body}')
        try:
            start = time.time()
            response = super().post(request, *args, **kwargs)
            end = time.time()
            logger.debug(f'Request succeed with code {response.status_code} for {end-start:.3f} seconds')
            return response
        except Exception as e:
            logger.error(f'Request failed with error: {e}')
            raise e



class GetLongURLAPIView(RetrieveAPIView):
    """
        Get original link from shorted
    """
    queryset = ShortedURL.objects.all()
    serializer_class = ShortedURLSerializer
    lookup_url_kwarg = 'shorted_url'
    lookup_field = 'shorted_url'
    

    def retrieve(self, request, *args, **kwargs):
        instance: ShortedURL = self.get_object()
        # if the link is expiered return the message
        if instance.expiration_date < datetime.now().date():
            return Response(data={'shorted_url': 'expiered'}, status=status.HTTP_410_GONE)
        # Increasing click count
        instance.click_count += 1
        instance.save(update_fields=['click_count'])
        return redirect(instance.original_url)
    
    def get(self, request: HttpRequest, *args, **kwargs):
        logger.dedbug(f'{request.method} {request.path} {request.GET}')
        try:
            start = time.time()
            response = super().get(request, *args, **kwargs)
            end = time.time()
            logger.debug(f'Request succeed with code {response.status_code} for {end-start:.3f} seconds')
            return response
        except Exception as e:
            logger.error(f'Request failed with error {e}')
            raise e