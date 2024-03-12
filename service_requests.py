from django.urls import path
from . import views

urlpatterns = [
    path('', views.service_requests, name='service_requests'),
    path('submit/', views.submit_service_request, name='submit_service_request'),
    path('track/', views.track_service_request, name='track_service_request'),
]