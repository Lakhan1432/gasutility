# settings.py
INSTALLED_APPS = [
    # ...
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',  # User account management
    'service_requests',  # Service request management
]

# urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('service_requests/', include('service_requests.urls')),
]

# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone_number = models.CharField(max_length=15)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2)

# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('account/', views.account, name='account'),
]

# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import User

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('service_requests:submit_service_request')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def logout(request):
    logout(request)
    return redirect('accounts:login')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        user = User.objects.create_user(username, email, phone_number, password)
        login(request, user)
        return redirect('service_requests:submit_service_request')
    return render(request, 'register.html')

def account(request):
    user = request.user
    return render(request, 'account.html', {'user': user})

# service_requests/models.py
from django.db import models
from accounts.models import User

class ServiceRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=50)
    details = models.TextField()
    files = models.FileField(upload_to='service_request_files/')
    status = models.CharField(max_length=50, default='Pending')
    date_submitted = models.DateTimeField(auto_now_add=True)
    date_resolved = models.DateTimeField(blank=True, null=True)

# service_requests/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('submit_service_request/', views.submit_service_request, name='submit_service_request'),
    path('track_service_request/', views.track_service_request, name='track_service_request'),
]

# service_requests/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ServiceRequest
from accounts.models import User

@login_required
def submit_service_request(request):
    if request.method == 'POST':
        user = request.user
        request_type= request.POST['request_type']
        details = request.POST['details']
        files = request.FILES['files']
        service_request = ServiceRequest(user=user, request_type=request_type, details=details, files=files)
        service_request.save()
        messages.success(request, 'Service request submitted successfully')
        return redirect('service_requests:track_service_request')
    return render(request, 'submit_service_request.html')

@login_required
def track_service_request(request):
    user = request.user
    service_requests = ServiceRequest.objects.filter(user=user)
    return render(request, 'track_service_request.html', {'service_requests': service_requests})