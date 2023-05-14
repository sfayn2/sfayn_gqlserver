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
    discount_type = models.ForeignKey(
            ContentType, 
            on_delete=models.CASCADE, 
            help_text="Select a discount rules for shop, tags, or any product variants",
            limit_choices_to={"app_label": "discount"}, #how to exclude self
    )
    object_id = models.PositiveIntegerField()
    discount_object = GenericForeignKey("discount_type", "object_id")
    vendor = models.ManyToManyField('vendor.Vendor', blank=True, related_name="vendor2discount")
    tag = models.ManyToManyField('tag.Tag', blank=True, related_name="tag2discount")
    shipping_method = models.ManyToManyField('shipping.Method', blank=True, related_name="shipmethod2discount")
    product_variant = models.ManyToManyField('product.VariantItem', blank=True, related_name="prodvariant2discount")
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


class DiscountTypeAbstract(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    start_date = models.DateTimeField() 
    end_date = models.DateTimeField() 
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE, 
    )
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name

    class Meta:
        abstract = True



class DiscountTypePercentageOrFixAmount(DiscountTypeAbstract):
    minimum_quantity = models.IntegerField(null=True)
    by_percentage = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            null=True, 
            blank=True, 
            help_text="Discount by percentage", 
        )
    fix_amount = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            null=True, 
            blank=True, 
            help_text="Discount by fix amount", 
        )


class DiscountTypeBuyXGetX(DiscountTypeAbstract):
    buy_quantity = models.IntegerField(null=True)
    get_quantity = models.IntegerField(null=True)


class DiscountTypeVoucher(DiscountTypeAbstract):
    voucher = models.CharField(max_length=15, help_text="Need to enter the voucher to use")
    percent_offer = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            null=True, 
            blank=True, 
            help_text="N% offer", 
        )
    fix_offer = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            null=True, 
            blank=True, 
            help_text="fix amount offer", 
        )
    min_spend = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            null=True, 
            blank=True, 
            help_text="min amount spend", 
        )
    capped_at = models.DecimalField(
            decimal_places=settings.DEFAULT_DECIMAL_PLACES, 
            max_digits=settings.DEFAULT_MAX_DIGITS,
            null=True, 
            blank=True, 
            help_text="max discount price", 
        )
    free_shipping = models.BooleanField(default=False, help_text="select for free shipping")
    usage_limit = models.IntegerField(default=1, help_text="limited to number of use")
    img_upload = models.ImageField(upload_to=path_and_rename, null=True, blank=True, help_text="Voucher img")

