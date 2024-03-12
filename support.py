from django.urls import path
from . import views

urlpatterns = [
    path('', views.support_dashboard, name='support_dashboard'),
    path('view/<int:request_id>/', views.view_request, name='view_request'),
    path('resolve/<int:request_id>/', views.resolve_request, name='resolve_request'),
]