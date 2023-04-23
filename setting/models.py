from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

# Create your models here.
class Setting(Site):

    class ProductApprovalType(models.IntegerChoices):
        PENDING_REVIEW = 0
        APPROVED = 1
        REJECTED = 2
        
    weight_unit = models.CharField(null=True, max_length=5, help_text="all products weight unit will be default in {weight_unit}") 
    dimensions_unit = models.CharField(null=True, max_length=5, help_text="all products weight unit will be default in {dimensions_unit}") 
    product_approval = models.IntegerField(default=1, choices=ProductApprovalType.choices, help_text="when product is created it requires approval before it can be published?") 
    country = models.CharField(null=True, blank=True, max_length=25, help_text="Singapore, .. ?") 
    currency = models.CharField(null=True, blank=True, max_length=10, help_text="USD, SGD, ..") 
    multi_vendor = models.BooleanField(default=1, help_text="allow external sellers")
    #commision??
    #payment schedule?
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="user2settings"
    )
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name
