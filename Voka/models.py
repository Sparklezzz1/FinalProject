from django.db import models

class Services(models.Model):
    title = models.CharField(max_length=60)
    content = models.TextField(blank=True)
    price = models.FloatField(null=True, blank=True)
    availability = models.BooleanField(default=True)