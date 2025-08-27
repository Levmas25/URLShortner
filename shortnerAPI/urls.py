from django.contrib import admin
from django.urls import path, include

from .views import URLShortnerAPIView, GetLongURLAPIView

app_name = 'api'

urlpatterns = [
    path('shorten/', URLShortnerAPIView.as_view()),
    path('<shorted_url>/', GetLongURLAPIView.as_view()),
]
