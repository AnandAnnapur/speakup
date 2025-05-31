from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Complaint
        fields = ['description', 'password']