from django.db import models
from django.contrib.auth.models import User


class ProcessedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_time = models.DateTimeField()
    status = models.BooleanField(default=False)
    input_file_path = models.CharField(max_length=255)
    wav_file_path = models.CharField(max_length=255)
