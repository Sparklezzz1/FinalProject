from django import forms
from .models.appointment import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ("status",)

