from django.db import models
from django.conf import settings
from decimal import Decimal

# Create your models here.
class Zone(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, help_text="ex. Zone 1")
    country = models.CharField(max_length=50, help_text="ex. Singapore")
    region = models.CharField(max_length=50, help_text="ex. Tampines")

    # offer shipping method on the same zone
    shipping_method = models.ManyToManyField('shipping.Method', related_name="method2zone", blank=True)

    created_by = models.ForeignKey(
        "auth.User", 
        null=True,
        blank=True,
        on_delete=models.CASCADE, 
        related_name="user2zone"
    )
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f'{self.name} {self.country}, {self.region}'


class Provider(models.Model):  #Fulfillment svc or Carrier or DropShip?

    name = models.CharField(max_length=20) 
    company_url = models.CharField(max_length=200, blank=True, null=True)
    tracker_url = models.CharField(max_length=200, blank=True, null=True)
    thumbnail_url = models.CharField(max_length=300, blank=True, null=True, help_text="thumbnail url")
    is_active = models.BooleanField(default=False)
    created_by = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="user2carrier")
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.name} ({self.company_url})"


class Method(models.Model):
    id = models.AutoField(primary_key=True)
    #tax 1 to many?
    name = models.CharField(max_length=50, help_text="ex. Free shipping, Local pickup")
    desc = models.CharField(max_length=150, blank=True, null=True)

    # removed external dependencies to self-contained shipping module? handle the composition of offers shipping method in frontend??

    ## offer shipping method only on the selected vendor?
    #vendor = models.ManyToManyField('vendor.Vendor', blank=True, related_name="vendor2method")

    ## offer shipping method only on the same tag?
    #tag = models.ManyToManyField('tag.Tag', blank=True, related_name="tag2method")

    ## offer shipping method only on the selected items?
    #product_variant = models.ManyToManyField('product.VariantItem', blank=True, related_name="prodvariant2method")

    ## offer shipping method only on the selected category?
    #category = models.ManyToManyField('product.Category', blank=True, related_name="category2method")

    #get the shipping cost based on classification
    rates = models.TextField(
            help_text="ex. [{ 'name': '3 hours express', 'max_Weight_kg': 1, min_LWH_cm: 60, 'cost':  14 }, { 'name': 'Specific Delivery Slot', 'max_Weight_kg': 1, min_LWH_cm: 60, 'cost':  18 }, ]",
            blank=True,
            null=True
        )

    #get the shipping cost based on provider calculate rate
    #fulfillment provider or carrier?
    provider = models.ForeignKey(
        'shipping.Provider', 
        null=True,
        blank=True,
        on_delete=models.CASCADE, 
        related_name="provider2method"
    )

    is_enable = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        "auth.User", 
        null=True,
        blank=True,
        on_delete=models.CASCADE, 
        related_name="user2method"
    )
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f'{self.title} {self.desc}, {self.cost}'

