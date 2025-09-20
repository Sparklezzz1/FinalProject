from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator

class AvailabilityManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(availability=Services.Status.PUBLISHED)
    

class Services(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, "Услуга не доступна"
        PUBLISHED = 1, "Услуга доступна"

    title = models.CharField(verbose_name="Услуга", max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    content = models.TextField(verbose_name="Описание",blank=True)
    price = models.FloatField(verbose_name="Стоимость",null=True, blank=True)
    time_create=models.DateTimeField(verbose_name="Время создания",auto_now_add=True)
    time_update=models.DateTimeField(verbose_name="Время изменения",auto_now=True)
    availability = models.IntegerField(verbose_name="Доступность услуги",choices=Status.choices, default=Status.PUBLISHED)
    direction = models.ForeignKey('Direction', on_delete=models.PROTECT)
    doctors = models.ManyToManyField('Doctors', blank=True,related_name="services")

    objects = models.Manager()
    is_availability = AvailabilityManager()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('serv', kwargs={'serv_slug' : self.slug})

class Direction(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255,unique=True,db_index=True)

    def __str__(self):
        return self.name
    
    
class Doctors(models.Model):
    name = models.CharField(verbose_name="Имя",max_length=255,db_index=True)
    surname = models.CharField(verbose_name="Фамилия",max_length=255)
    patronymic = models.CharField(verbose_name="Отчество",max_length=255)
    job_title = models.CharField(verbose_name="Должность",max_length=255,null=True,blank=True)
    experience = models.IntegerField(verbose_name="Стаж работы", default=0,)
    slug = models.SlugField(max_length=255,unique=True,db_index=True)

    def __str__(self):
         return f"{self.surname} {self.name} {self.patronymic}"
         
    def get_absolute_url(self):
        return reverse('doc', kwargs={'doc_slug' : self.slug})
    

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('confirmed', 'Подтверждена'),
        ('canceled', 'Отменена'),
        ('done', 'Завершена'),
    ]
    patient_name = models.CharField(verbose_name="Имя пациента", max_length=255, db_index=True)
    patient_surname = models.CharField(verbose_name="Фамилия пациента", max_length=255, db_index=True)
    doctor = models.ForeignKey("Doctors", on_delete=models.CASCADE, related_name="appointments")
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
        unique_together = ('doctor', 'date', 'time')
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.patient_surname} {self.patient_name} : {self.doctor} ({self.date} {self.time})"