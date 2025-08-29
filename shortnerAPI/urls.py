from django.contrib import admin
from django.urls import path, include, re_path

from .views import URLShortnerAPIView, GetLongURLAPIView

app_name = 'api'

urlpatterns = [
    re_path('^shorten/$', URLShortnerAPIView.as_view(), name='shorten_url'),
    re_path(r'^(?<shorted_url>[a-zA-Z0-9]+){1,15}/$', GetLongURLAPIView.as_view(), name='get_orginal_url'),
]
