from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from slugify import slugify

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
    direction = models.ForeignKey('Direction',verbose_name="Направление", on_delete=models.PROTECT)
    doctors = models.ManyToManyField('Voka.Doctors',verbose_name="Время создания", blank=True,related_name="services")

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.slug: 
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('serv', kwargs={'serv_slug' : self.slug})

class Direction(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255,unique=True,db_index=True)

    def __str__(self):
        return self.name
    
    

    

