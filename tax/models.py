from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tax(models.Model):

    class Status(models.IntegerChoices):
        ACTIVE = 0
        IN_ACTIVE = 1

    name = models.CharField(max_length=20, help_text="GST, VAT, ?")
    country = models.CharField(max_length=50)
    #region = models.CharField(max_length=50) by state or region??
    rate = models.FloatField(null=True, blank=True, help_text="N% tax rate per order?", verbose_name="Rate(%)")
    status = models.IntegerField(null=True, choices=Status.choices) 
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2tax")
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.name} {self.rate}%"

