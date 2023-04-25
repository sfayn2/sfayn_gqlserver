from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Zone(models.Model):
    id = models.AutoField(primary_key=True)
    #method = models.ForeignKey('shipping.Method', on_delete=models.CASCADE, related_name="method2zone", blank=True, null=True)
    name = models.CharField(max_length=50, help_text="ex. Zone 1")
    country = models.CharField(max_length=50, help_text="ex. Singapore")
    region = models.CharField(max_length=50, help_text="ex. Tampines")
    created_by = models.ForeignKey(
        User, 
        null=True,
        blank=True,
        on_delete=models.CASCADE, 
        related_name="user2zone"
    )
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f'{self.name} {self.country}, {self.region}'


#class Dimensions(models.Model):
#    weight
#    package_length
#    package_width
#    package_depth

class Method(models.Model):
    id = models.AutoField(primary_key=True)
    zone = models.ManyToManyField('shipping.Zone', related_name="zone2method", blank=True)
    #TODO: shipping carrier and duties  & tax??
    #carrier 1 to many?
    #tax 1 to many?
    title = models.CharField(max_length=50, help_text="ex. Free shipping, Local pickup")
    desc = models.CharField(max_length=150)
    cost = models.FloatField(null=True, blank=True, help_text="cost or overall cost?")
    enable = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User, 
        null=True,
        blank=True,
        on_delete=models.CASCADE, 
        related_name="user2method"
    )
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f'{self.title} {self.desc}, {self.cost}'


#class Carrier(models.Model):
#    api?


