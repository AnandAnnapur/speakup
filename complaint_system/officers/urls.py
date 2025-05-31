# officers/urls.py
from django.urls import path
from . import views

app_name = 'officers' # <--- THIS IS CRUCIAL AND MUST BE AT THE TOP

urlpatterns = [
    # ... your URL patterns ...
    path('signup/', views.officer_signup, name='officer_signup'),
    path('login/', views.officer_login, name='officer_login'),
    path('logout/', views.officer_logout, name='officer_logout'),
    path('dashboard/', views.complaint_dashboard, name='complaint_dashboard'),
    path('update-status/<int:pk>/', views.update_complaint_status, name='update_complaint_status'),
    path('create/', views.create_complaint, name='create_complaint'),
    path('status/', views.check_status, name='check_status'),
]