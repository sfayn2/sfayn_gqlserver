from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Discount(models.Model):
    class Status(models.IntegerChoices):
        ENABLED = 1

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    minimum_quantity = models.IntegerField(null=True)
    discount_price = models.FloatField(null=True, blank=True, help_text="Discount by Price")
    discount_percentage = models.FloatField(null=True, blank=True, help_text="Discount by percentage")
    start_date = models.DateTimeField() 
    end_date = models.DateTimeField() 
    status = models.IntegerField(
        blank=True, 
        null=True, 
        default=True,
        choices=Status.choices
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE, 
        related_name="user2discount"
    )
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name
