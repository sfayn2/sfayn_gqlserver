from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site

# Create your models here.
class ShopProfile(Site):
    #shop = models.OneToOneField(Site, on_delete=models.CASCADE, related_name="shopprofile")
    shop_desc = models.CharField(null=True, max_length=50) 
    group = models.ForeignKey(
        Group, 
        null=True,
        blank=True,
        on_delete=models.CASCADE, 
        related_name="grp2shopprofile"
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="user2shopprofile"
    )
    product = models.ManyToManyField('product.ProductParent', blank=True, related_name="prod2shop")

    #category = models.ManyToManyField('product.ProductCategory', blank=True, related_name="category2shop")
    promotional_banner = models.ManyToManyField('promotional.PromotionalBanner', blank=True, related_name="banner2shop")
    #what else?
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name


# TODO: to obsolete just handle Cart in front end
class ShopCart(models.Model):
    id = models.AutoField(primary_key=True)
    product_variant = models.ForeignKey(
        'product.ProductVariantItem', 
        on_delete=models.CASCADE, 
        related_name="prodvariant2cart"
    )
    quantity = models.IntegerField(null=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="user2cart"
    )
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return "ProductionVariantItem({}) Qty({})".format(self.product_variant, self.quantity)

# TODO: moved to Order models
class ShopOrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(
        "shop.ShopOrder", 
        on_delete=models.CASCADE,
        related_name="order2orderitem", 
        null=True, 
        blank=True
    )
    shopcart = models.OneToOneField(
        "shop.ShopCart", 
        on_delete=models.CASCADE,
        related_name="cart2orderitem", 
        null=True, 
        blank=True
    ) 
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE, 
        related_name="user2orderitem"
    )
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return "Order({}) ShopCart({})".format(self.order, self.shopcart)


# TODO: moved to Order models
class ShopOrder(models.Model):

    class Status(models.IntegerChoices):
        WAITING_FOR_PAYMENT = 0
        PAID = 1
        PROCESSING = 2
        SHIPPED_OUT = 3
        REFUNDED = 4
        CANCEL = 5
        COMPLETED = 6

    id = models.AutoField(primary_key=True)
    payment_method = models.ForeignKey(
        "payment.PaymentMethod", 
        on_delete=models.CASCADE,
        related_name="payment2order", 
        null=True, 
        blank=True
    )
    customer_address = models.ForeignKey(
        "customer.CustomerAddress", 
        on_delete=models.CASCADE,
        related_name="customer2order", 
        null=True, 
        blank=True
    )
    total_amount = models.FloatField(null=True, blank=True)
    status = models.IntegerField(
        blank=True, 
        null=True, 
        choices=Status.choices
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="user2order"
    )
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return "PaymentMethod({}) CustomerAddress({}) TotalAmount({}) Status({})".format(
            self.payment_method,
            self.customer_address,
            self.total_amount,
            self.status
        )


