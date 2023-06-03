from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User, Group
from utils import path_and_rename
from django.conf import settings

# Create your models here.
class Discount(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)

    # should front end code to the handling of each rules?
    discount_types = models.TextField(
            help_text="ex. [ {'name': 'Discount by Fix or Percentage', 'by_percentage': 12 }, { 'name': 'Buy N get N', 'buy_qty': 5, 'get_qty': 1 } ]",
            blank=True,
            null=True
    )

    # offer discount types to selected vendor? 
    vendor = models.ManyToManyField('accounts.Vendor', blank=True, related_name="vendor2discount")

    # offer to selected tag products?
    tag = models.ManyToManyField('product.Tag', blank=True, related_name="tag2discount")

    # offer to selected ship method?
    shipping_method = models.ManyToManyField('shipping.Method', blank=True, related_name="shipmethod2discount")

    # offer to selected product variant?
    product_variant = models.ManyToManyField('product.VariantItem', blank=True, related_name="prodvariant2discount")

    # offer to all selected category?
    category = models.ManyToManyField('product.Category', blank=True, related_name="category2discount")

    is_enable = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE, 
        related_name="user2discount"
    )
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name



