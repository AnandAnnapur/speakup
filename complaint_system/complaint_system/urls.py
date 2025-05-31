"""
Main URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from officers import views as officers_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',officers_views.home, name='home'),  # Redirect root to home view
    path('', include('officers.urls')),    # Redirect root to our app
]