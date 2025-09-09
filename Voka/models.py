from django.db import models
from django.urls import reverse

class AvailabilityManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(availability=Services.Status.PUBLISHED)
    

class Services(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, "Услуга не доступна"
        PUBLISHED = 1, "Услуга доступна"

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    content = models.TextField(blank=True)
    price = models.FloatField(null=True, blank=True)
    time_create=models.DateTimeField(auto_now_add=True)
    time_update=models.DateTimeField(auto_now=True)
    availability = models.IntegerField(choices=Status.choices, default=Status.PUBLISHED)
    direction = models.ForeignKey('Direction', on_delete=models.PROTECT)

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
    
    def get_absolute_url(self):
        return reverse('show_direction', kwargs={'direction_slug':self.slug})
    