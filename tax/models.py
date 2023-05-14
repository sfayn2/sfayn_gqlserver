from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Tax(models.Model):

    name = models.CharField(max_length=20, help_text="GST, VAT, ?")
    country = models.CharField(max_length=50)
    region = models.CharField(max_length=50, blank=True, null=True) #by state or region??
    rate = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            null=True, 
            blank=True, 
            help_text="N% tax rate",
            verbose_name="Rate(%)"
        )
    is_active = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2tax")
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.name} {self.rate}%"

