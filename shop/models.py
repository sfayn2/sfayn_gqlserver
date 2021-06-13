from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ShopCart(models.Model):
    id = models.AutoField(primary_key=True)
    product_variant = models.ForeignKey('product.ProductVariant', on_delete=models.CASCADE, related_name="prodvariant2cart")
    quantity = models.IntegerField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2cart")
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    class Meta:
        unique_together = ("product_variant", "created_by")

