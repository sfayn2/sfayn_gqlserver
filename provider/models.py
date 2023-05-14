from django.db import models
from django.contrib.auth.models import User
from utils import path_and_rename
from django.conf import settings
from decimal import Decimal

# Create your models here.
class Provider(models.Model): #Fulfillment service / Carrier / Warehouse

    name = models.CharField(max_length=20) #can be outsource?
    address = models.TextField(blank=True, null=True)
    postal = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)
    company_url = models.CharField(max_length=200, blank=True, null=True)
    tracker_url = models.CharField(max_length=200, blank=True, null=True)
    logo = models.ImageField(upload_to=path_and_rename, null=True, blank=True, help_text="company logo")
    handling_fee = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            null=True, 
            blank=True, 
            help_text="Add handling fee ", 
            default=Decimal("0.0")
        )
    is_active = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2provider")
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.name} ({self.company_url})"
