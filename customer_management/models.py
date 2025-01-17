from django.contrib.auth.models import User
from django.db import models
import uuid

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="customer"
    )

    #allows us t odecouple the customer data from User model?
    customer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #uuid for external integration
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.user.email}"

class Address(models.Model):
    ADDRESS_TYPE_CHOICES = (
        ('billing', 'Billing'),
        ('shipping', 'Shipping'),
    )

    customer = models.ForeignKey(
        Customer,
        related_name="addresses",
        on_delete=models.CASCADE
    )

    address_type = models.CharField(
        max_length=10,
        choices=ADDRESS_TYPE_CHOICES
    )

    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=10, blank=True, null=True)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.address_type.capitalize()} Address: {self.street}, {self.city}, {self.country}"

    class Meta:
        unique_together = ('customer', 'address_type', 'is_default') #ensure one default per addres type