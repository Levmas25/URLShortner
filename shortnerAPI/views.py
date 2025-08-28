import logging

from django.shortcuts import redirect
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
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