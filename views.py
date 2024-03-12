from django.shortcuts import render, redirect
from .models import ServiceRequest
from accounts.models import User
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ServiceRequest
from accounts.models import User

def service_requests(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    service_requests = ServiceRequest.objects.filter(user=user)
    return render(request, 'service_requests.html', {'service_requests': service_requests})

def submit_service_request(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        user = request.user
        request_type = request.POST['request_type']
        details = request.POST['details']
        files = request.FILES['files']
        service_request = ServiceRequest(user=user, request_type=request_type, details=details, files=files)
        service_request.save()
        messages.success(request, 'Service request submitted successfully')
        return redirect('service_requests')
    return render(request, 'submit_service_request.html')

def track_service_request(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    service_requests = ServiceRequest.objects.filter(user=user)
    return render(request, 'track_service_request.html', {'service_requests': service_requests})



def support_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('login')
    service_requests = ServiceRequest.objects.all()
    return render(request, 'support_dashboard.html', {'service_requests': service_requests})

def view_request(request, request_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('login')
    service_request = ServiceRequest.objects.get(id=request_id)
    return render(request, 'view_request.html', {'service_request': service_request})

def resolve_request(request, request_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('login')
    service_request = ServiceRequest.objects.get(id=request_id)
    service_request.status = 'Resolved'
    service_request.date_resolved = timezone.now()
    service_request.save()
    messages.success(request, 'Service request resolved successfully')
    return redirect('support_dashboard')