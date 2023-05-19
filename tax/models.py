from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Tax(models.Model):

    name = models.CharField(max_length=20, help_text="GST, VAT, ?")
    rates = models.TextField(
            help_text="ex. [{ 'name': 'Standard Rate', 'country': 'SGP', 'percentage':  8 } ]",
            blank=True,
            null=True
        )
    is_active = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2tax")
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.name} {self.rate}%"

