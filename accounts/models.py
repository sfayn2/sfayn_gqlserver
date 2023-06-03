from django.db import models
from django.contrib.auth.models import User, Group
from utils import path_and_rename

# Create your models here.
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2address")
    address = models.TextField()
    postal = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    default_shipping = models.BooleanField(default=False, help_text="set as default shipping address")
    default_billing = models.BooleanField(default=False, help_text="set as default billing address")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_by2address")
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.address} {self.postal} {self.country}, {self.region}"


class GroupProfile(Group):
    role = models.ManyToManyField("accounts.Role", related_name="role2group")
    desc = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2group")
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def get_roles(self):
        return ", ".join(list(self.role.values_list('name', flat=True)))


    def __str__(self):
        return f"{self.name} - {self.desc} ({self.get_roles()})"


class Role(models.Model):
    name = models.CharField(max_length=20, help_text="ex. VENDOR")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2role")
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name

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

