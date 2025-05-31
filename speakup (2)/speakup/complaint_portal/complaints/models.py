from django.db import models

class Complaint(models.Model):
    complaint_number = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    password = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default="Pending")

    def __str__(self):
        return f"{self.complaint_number}"