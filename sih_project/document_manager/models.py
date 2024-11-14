# models.py
from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    file_id = models.CharField(max_length=100)
    ocr_text = models.TextField(blank=True, null=True)
    filename = models.CharField(max_length=255)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.filename
