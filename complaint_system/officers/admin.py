"""
Admin site configuration
"""
from django.contrib import admin
from .models import ComplaintOfficer, Complaint

@admin.register(ComplaintOfficer)
class ComplaintOfficerAdmin(admin.ModelAdmin):
    list_display = ['email', 'created_at']
    search_fields = ['email']
    list_filter = ['created_at']

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['complaint_id', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['complaint_id', 'description']
    readonly_fields = ['complaint_id', 'created_at']