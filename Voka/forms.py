from django import forms
from .models.appointment import Appointment
from django.forms.widgets import DateInput

class AppointmentForm(forms.ModelForm):
    date = forms.DateField(
        widget=DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',  
            }
        ),
        label="Дата приема"
    )
    time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                'type': 'time', 
                'class': 'form-control'
            }
        ),
        label="Время приёма"
    )
    class Meta:
        model = Appointment
        exclude = ("status",)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

