from django.db import models
from django.contrib.auth.models import User, Group

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

