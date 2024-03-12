from django.db import models
from accounts.models import User

class ServiceRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=255)
    details = models.TextField()
    files = models.FileField(upload_to='service_request_files/')
    status = models.CharField(max_length=255, default='Pending')
    date_submitted = models.DateTimeField(auto_now_add=True)
    date_resolved = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.request_type