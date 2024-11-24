from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class Person(AbstractUser):
    USER_TYPE_CHOICES = [
        ('ops', 'Ops User'),
        ('client', 'Client User'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    email_verified = models.BooleanField(default=False)

    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='custom_user_permissions',
        blank=True
    )

    def __str__(self):
        return self.username


class UploadedFile(models.Model):
    uploaded_by = models.ForeignKey(Person, on_delete=models.CASCADE, limit_choices_to={'user_type': 'ops'})
    file = models.FileField(upload_to='uploads/', null=False)#, blank=True)  # Temporarily nullable
    file_type = models.CharField(max_length=10, choices=[('pptx', 'PowerPoint'), ('docx', 'Word Document'), ('xlsx', 'Excel Spreadsheet')])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} uploaded by {self.uploaded_by.username}"
