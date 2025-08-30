from django.contrib import admin
from django.urls import path, include, re_path

from .views import URLShortnerAPIView, GetLongURLAPIView

app_name = 'api'

urlpatterns = [
    re_path(r'^shorten/$', URLShortnerAPIView.as_view(), name='shorten_url'),
    path('<shorted_url>/', GetLongURLAPIView.as_view(), name='get_original_url'),
]
