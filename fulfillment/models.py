from django.db import models
from django.contrib.auth.models import User
from utils.utils import path_and_rename

# Create your models here.
class Fulfillment(models.Model): #Fulfillment service

    class Status(models.IntegerChoices):
        ACTIVE = 0
        IN_ACTIVE = 1

    name = models.CharField(max_length=20) #can be outsource?
    company_url = models.CharField(max_length=200, blank=True, null=True)
    tracker_url = models.CharField(max_length=200, blank=True, null=True)
    logo = models.ImageField(upload_to=path_and_rename, null=True, blank=True, help_text="company logo")
    manage_fulfillment = models.BooleanField(default=True, help_text="DIY managed your own fulfillment")
    status = models.IntegerField(null=True, choices=Status.choices) 
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2fulfillment")
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.name} {self.get_display_status()}"

