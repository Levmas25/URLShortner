from django.contrib import admin
from django.urls import path, include

from .views import URLShortnerAPIView, GetLongURLAPIView

app_name = 'api'

urlpatterns = [
    path('shorten/', URLShortnerAPIView.as_view(), name='shorten_url'),
    path('<shorted_url>/', GetLongURLAPIView.as_view(), name='get_orginal_url'),
]
