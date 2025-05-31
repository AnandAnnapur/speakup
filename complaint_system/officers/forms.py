"""
Forms for officer authentication and complaint management
"""
from django import forms
from django.contrib.auth.hashers import make_password
from .models import ComplaintOfficer, Complaint


class OfficerSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
   
    class Meta:
        model = ComplaintOfficer
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
   
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
       
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
       
        return cleaned_data
   
    def save(self, commit=True):
        officer = super().save(commit=False)
        officer.set_password(self.cleaned_data['password'])
        if commit:
            officer.save()
        return officer


class OfficerLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class ComplaintStatusForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'})
        }


class ComplaintForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'shadow appearance-none border rounded-lg w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-blue-500'
            }
        ),
        label="Password",
        help_text="Choose a strong password for checking your complaint status."
    )

    class Meta:
        model = Complaint
        fields = ['username', '_description', 'password']
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'shadow appearance-none border rounded-lg w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-blue-500'
                }
            ),
            '_description': forms.Textarea(
                attrs={
                    'class': 'shadow appearance-none border rounded-lg w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-blue-500',
                    'rows': 4
                }
            ),
        }

    def save(self, commit=True):
        # Create the complaint instance without saving to DB yet
        complaint = super().save(commit=False)
        # Hash the password directly from the cleaned data and assign it to password_hash
        complaint.password_hash = make_password(self.cleaned_data['password'])

        # Ensure username defaults to 'anonymous' if not provided
        if not complaint.username:
            complaint.username = 'anonymous'

        if commit:
            complaint.save()
        return complaint
