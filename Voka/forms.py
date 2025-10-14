from django import forms
from django.contrib.auth.models import User 
from .models.appointment import Appointment
from .models.services import Services
from django.forms.widgets import DateInput
from django.utils.translation import gettext_lazy as _

class AppointmentForm(forms.ModelForm):
    date = forms.DateField(
        widget=DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',  
            }
        ),
        label=_("Дата приема")
    )
    time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                'type': 'time', 
                'class': 'form-control'
            }
        ),
        label=_("Время приёма")
    )
    class Meta:
        model = Appointment
        exclude = ("status",)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class ServicesForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = '__all__'
        exclude = ("slug",)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class RegistrationForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    repeat_password = forms.CharField()

    def save(self):
        same_name_users = User.objects.filter(username=self.cleaned_data["username"]).exists()
        if not same_name_users and self.cleaned_data["password"] == self.cleaned_data["repeat_password"]:
            user = User(username=self.cleaned_data["username"])
            user.set_password(self.cleaned_data["password"])  
            user.save()
            return user
        return None