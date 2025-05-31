from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import uuid
from datetime import timedelta
from django.utils import timezone
from .encryption import encrypt_text, decrypt_text


class ComplaintOfficer(models.Model):
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def set_password(self, password):
        self.password_hash = make_password(password)
    
    def check_password(self, password):
        return check_password(password, self.password_hash)
    
    def __str__(self):
        return self.email


class Complaint(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
    ]

    complaint_id = models.CharField(max_length=12, unique=True, editable=False)
    username = models.CharField(max_length=150, default='anonymous')
    _description = models.TextField(db_column='description')  # encrypted at rest
    password_hash = models.CharField(max_length=128)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.complaint_id:
            self.complaint_id = str(uuid.uuid4()).replace('-', '')[:12].upper()

        if hasattr(self, '_raw_password') and self._raw_password:
            self.password_hash = make_password(self._raw_password)
            self._raw_password = None

        super().save(*args, **kwargs)

    @property
    
    def description(self):
        try:
            if not self._description:
                return ""
            return decrypt_text(self._description)
        except Exception as e:
            print(f"Decryption failed for complaint {self.complaint_id}: {e}")
            # Return the raw data or a placeholder
            return f"[Decryption failed: {str(e)}]"
    @description.setter
    def description(self, value):
        self._description = encrypt_text(value)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

    def __str__(self):
        return f"Complaint {self.complaint_id} - {self.username}"

    @classmethod
    def delete_old_completed(cls):
        one_month_ago = timezone.now() - timedelta(days=30)
        cls.objects.filter(
            status='Completed',
            created_at__lt=one_month_ago
        ).delete()
