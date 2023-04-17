from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
class Discount(models.Model):
    class Status(models.IntegerChoices):
        ENABLED = 1

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
    shop = models.ManyToManyField('shop.ShopProfile', blank=True, related_name="shop2discount")
    tag = models.ManyToManyField('tag.Tag', blank=True, related_name="tag2discount")
    product_variant = models.ManyToManyField('product.ProductVariantItem', blank=True, related_name="prodvariant2discount")
    category = models.ManyToManyField('product.ProductCategory', blank=True, related_name="category2discount")
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
    by_percentage = models.FloatField(null=True, blank=True, help_text="Discount by percentage")
    fix_amount = models.FloatField(null=True, blank=True, help_text="Discount by fix amount")


class DiscountTypeBuyXGetX(DiscountTypeAbstract):
    buy_quantity = models.IntegerField(null=True)
    get_quantity = models.IntegerField(null=True)


class DiscountTypeVoucher(DiscountTypeAbstract):
    voucher = models.CharField(max_length=15, help_text="Need to enter the voucher to use")
    min_spend = models.FloatField(null=True, blank=True, help_text="N% min spend")
    capped_at = models.FloatField(null=True, blank=True, help_text="Capped at N%")
    free_shipping = models.BooleanField(default=False, help_text="select for free shipping")
    use = models.BooleanField(default=False)

