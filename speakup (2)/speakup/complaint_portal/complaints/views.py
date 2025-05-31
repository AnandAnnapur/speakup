from django.shortcuts import render, redirect
from .forms import ComplaintForm
from .models import Complaint
from .utils import generate_complaint_number

def home(request):
    return render(request, 'complaints/home.html')

def create_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.complaint_number = generate_complaint_number()
            complaint.save()
            return render(request, 'complaints/complaint_success.html', {
                'complaint_number': complaint.complaint_number
            })
    else:
        form = ComplaintForm()
    return render(request, 'complaints/create_complaint.html', {'form': form})

def check_status(request):
    error = ""
    status = None
    if request.method == 'POST':
        complaint_number = request.POST.get('complaint_number')
        password = request.POST.get('password')
        try:
            complaint = Complaint.objects.get(complaint_number=complaint_number, password=password)
            status = complaint.status
        except Complaint.DoesNotExist:
            error = "Invalid complaint number or password."
    return render(request, 'complaints/check_status.html', {'status': status, 'error': error})