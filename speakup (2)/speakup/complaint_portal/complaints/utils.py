import random
import string
from .models import Complaint

def generate_complaint_number():
    while True:
        number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if not Complaint.objects.filter(complaint_number=number).exists():
            return number