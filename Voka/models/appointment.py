from Voka import models
from django.db import models
from django.core.validators import RegexValidator

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('confirmed', 'Подтверждена'),
        ('canceled', 'Отменена'),
        ('done', 'Завершена'),
    ]
    patient_name = models.CharField(verbose_name="Имя пациента", max_length=255, db_index=True)
    patient_surname = models.CharField(verbose_name="Фамилия пациента", max_length=255, db_index=True)
    services = models.ForeignKey("Voka.Services",verbose_name="Услуга",   null=True, 
        blank=True,on_delete=models.CASCADE,related_name="services_appointments")
    date = models.DateField(verbose_name="Дата приема", db_index=True)
    time = models.TimeField(verbose_name="Время приёма", db_index=True)
    reason = models.TextField(verbose_name="Причина визита", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    phone = models.CharField(verbose_name="Номер телефона",max_length=13,
        validators=[
            RegexValidator(
                regex=r'^\+375(?:25|29|33|44|17)\d{7}$',
                message="Введите корректный номер телефона"
            )
        ],
    )

    class Meta:
        unique_together = ('services', 'date', 'time')
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.patient_surname} {self.patient_name} : {self.services} ({self.date} {self.time})"