# officers/views.py
"""
View functions for complaint officer system
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import ComplaintOfficer, Complaint
from .forms import OfficerSignupForm, OfficerLoginForm, ComplaintStatusForm
from .forms import ComplaintForm
from .utils import generate_complaint_number

# Officer authentication views
def officer_signup(request):
    if request.method == 'POST':
        form = OfficerSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Officer account created successfully! Please login.')
            # CORRECTED: Use 'officers:officer_login' for namespaced URL
            return redirect('officers:officer_login')
    else:
        form = OfficerSignupForm()

    return render(request, 'officers/signup.html', {'form': form})

def officer_login(request):
    if request.method == 'POST':
        form = OfficerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                officer = ComplaintOfficer.objects.get(email=email)
                if officer.check_password(password):
                    request.session['officer_id'] = officer.id
                    request.session['officer_email'] = officer.email
                    messages.success(request, 'Login successful!')
                    # CORRECTED: Use 'officers:complaint_dashboard' for namespaced URL
                    return redirect('officers:complaint_dashboard')
                else:
                    messages.error(request, 'Invalid password.')
            except ComplaintOfficer.DoesNotExist:
                messages.error(request, 'Officer account not found.')
    else:
        form = OfficerLoginForm()

    return render(request, 'officers/login.html', {'form': form})

def officer_logout(request):
    request.session.flush()
    messages.success(request, 'Logged out successfully.')
    # CORRECTED: Use 'officers:officer_login' for namespaced URL
    return redirect('officers:officer_login')

# Complaint management views
def complaint_dashboard(request):
    # Check if officer is logged in
    if 'officer_id' not in request.session:
        messages.error(request, 'Please login to access the dashboard.')
        # CORRECTED: Use 'officers:officer_login' for namespaced URL
        return redirect('officers:officer_login')

    # Delete old completed complaints
    Complaint.delete_old_completed()

    # Get complaints by status
    pending_complaints = Complaint.objects.filter(status='Pending').order_by('-created_at')
    ongoing_complaints = Complaint.objects.filter(status='Ongoing').order_by('-created_at')
    completed_complaints = Complaint.objects.filter(status='Completed').order_by('-created_at')

    context = {
        'pending_complaints': pending_complaints,
        'ongoing_complaints': ongoing_complaints,
        'completed_complaints': completed_complaints,
        'officer_email': request.session.get('officer_email')
    }

    return render(request, 'officers/dashboard.html', context)

@require_http_methods(["POST"])
def update_complaint_status(request, pk):
    # Check if officer is logged in
    if 'officer_id' not in request.session:
        return JsonResponse({'success': False, 'error': 'Not authenticated'})

    complaint = get_object_or_404(Complaint, pk=pk)
    new_status = request.POST.get('status')

    if new_status in ['Pending', 'Ongoing', 'Completed']:
        complaint.status = new_status
        complaint.save()
        messages.success(request, f'Complaint {complaint.complaint_id} status updated to {new_status}.')
        # CORRECTED: Use 'officers:complaint_dashboard' for namespaced URL
        return redirect('officers:complaint_dashboard')

    messages.error(request, 'Invalid status update.')
    # CORRECTED: Use 'officers:complaint_dashboard' for namespaced URL
    return redirect('officers:complaint_dashboard')

def create_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            # The form's save method now handles hashing the password and
            # the model's save method will generate the complaint_id.
            complaint = form.save() # This now saves the complaint with hashed password
            # Assuming 'complaints/complaint_success.html' is a template, not a redirect
            return render(request, 'complaints/complaint_success.html', {
                'complaint_id': complaint.complaint_id
            })
        else:
            # If form is not valid, it will be rendered again with errors
            pass
    else:
        form = ComplaintForm()
    return render(request, 'complaints/create_complaint.html', {'form': form})

def check_status(request):
    error = ""
    status = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password') # This is the raw password from the form

        try:
            # Since username is no longer unique, we use filter() to get all matching complaints.
            # Then, we iterate to find one that matches the provided password.
            complaints = Complaint.objects.filter(username=username)
            found_complaint = None
            for complaint in complaints:
                if complaint.check_password(password):
                    found_complaint = complaint
                    break # Found a match, exit loop

            if found_complaint:
                status = found_complaint.status
            else:
                # Generic error for security, whether username doesn't exist or password is wrong
                error = "Invalid username or password."
        except Exception as e:
            # Catch any unexpected errors during the process
            error = "An error occurred. Please try again."
            print(f"Error in check_status: {e}") # Log the actual error for debugging

    return render(request, 'complaints/check_status.html', {
        'status': status,
        'error': error,
        'username_input': request.POST.get('username', '') # Keep username in input on error
    })

def home(request):
    # This will render your main landing page template from officers/templates/home/index.html
    return render(request,'home/index.html')