from django.db import models
from django.contrib.auth.models import User
from utils.utils import path_and_rename

# Create your models here.
class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    img_upload = models.ImageField(upload_to=path_and_rename, null=True, blank=True, help_text="Primary img")
    img_url = models.CharField(max_length=300, null=True, blank=True, help_text="secondary img") 
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2tags")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name


class TagItem(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.ForeignKey("tag.Tag", on_delete=models.CASCADE, null=True, related_name="tags2items", blank=True) 
    product_variant = models.ForeignKey("product.VariantItem", on_delete=models.CASCADE, null=True, related_name="variant2tags", blank=True) 
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2tagsitem")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return "Tag({}) Product({})".format(self.tag.name, self.product_variant)
