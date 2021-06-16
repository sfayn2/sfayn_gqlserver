from django.db import models
from django.contrib.auth.models import User


class CustomerAddress(models.Model):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=50)
    email = models.CharField(max_length=50, null=True)
    address = models.TextField()
    postal = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    default = models.BooleanField(default=False, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2addr")
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return "({}) Address({} {} {})".format(
            self.fullname, 
            self.address, 
            self.postal, 
            self.country
        )


