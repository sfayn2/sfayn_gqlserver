from django.db import models
from django.contrib.auth.models import User
from utils.utils import path_and_rename

# Create your models here.
# Create Entry for Muli Vendor option
class Vendor(models.Model):
    
    class Status(models.IntegerChoices):
        PENDING_REVIEW = 0
        APPROVED = 1
        REJECTED = 2

    name = models.CharField(max_length=20, help_text="Vendor's Name")
    desc = models.TextField(help_text="I sell what?")
    logo = models.ImageField(upload_to=path_and_rename, null=True, blank=True)
    status = models.IntegerField(null=True, choices=Status.choices, default=0) 
    created_by = models.OneToOneField(User, on_delete=models.CASCADE, related_name="owner2vendor", verbose_name="Owner") #1 account for single registered vendor
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.name} - {self.desc} ({self.get_status_display()})"

