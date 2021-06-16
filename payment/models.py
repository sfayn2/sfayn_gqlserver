from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#TODO yet to implement
class PaymentMethod(models.Model):
    id = models.AutoField(primary_key=True)
    method = models.CharField(max_length=50, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2paymentmethod")
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 


