from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_complaint, name='create_complaint'),
    path('status/', views.check_status, name='check_status'),
]