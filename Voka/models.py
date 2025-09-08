from django.db import models
from django.urls import reverse

class Services(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    content = models.TextField(blank=True)
    price = models.FloatField(null=True, blank=True)
    time_create=models.DateTimeField(auto_now_add=True)
    time_update=models.DateTimeField(auto_now=True)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    def get_asolute_url(self):
        return reverse('serv', kwargs={'serv_slug' : self.slug})