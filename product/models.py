from django.db import models
from django.contrib.auth.models import User
from utils.utils import path_and_rename


# Create your models here.
class ProductCategory(models.Model):

    class LevelChoices(models.IntegerChoices):
        LEVEL_1 = 1
        LEVEL_2 = 2
        LEVEL_3 = 3

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    level = models.IntegerField(null=True, choices=LevelChoices.choices) 
    img_upload = models.ImageField(upload_to=path_and_rename, null=True, blank=True, help_text="Primary img")
    img_url = models.CharField(max_length=300, null=True, blank=True, help_text="secondary img") #TODO imagefield
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2category")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return "Level({}) ParentId({}) Id({}) Name({})".format(self.level, self.parent_id, self.id, self.name, self.level)


class ProductParent(models.Model):

    class Status(models.IntegerChoices):
        INACTIVE = 0
        ACTIVE = 1

    #we can add more attributes later
    id = models.AutoField(primary_key=True)
    parent_sn = models.CharField(max_length=50) #CharField to accept multiple sku datatype 
    title = models.CharField(max_length=100, null=True) 
    category = models.ForeignKey("product.ProductCategory", on_delete=models.CASCADE, null=True, related_name="cat2product") 
    goods_brand = models.CharField(max_length=30, null=True, blank=True)
    goods_desc = models.TextField(null=True) 
    status = models.IntegerField(null=True, choices=Status.choices) 
    #publish = models.BooleanField(default=False) 
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2product")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return "ParentSn:{} Title:{}".format(self.parent_sn, self.title)


class ProductVariant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2variant")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name


class ProductVariantItem(models.Model):
    id = models.AutoField(primary_key=True)
    product_variant = models.ForeignKey("product.ProductVariant", on_delete=models.CASCADE, null=True, related_name="variant2item", blank=True) 
    parent_sn = models.ForeignKey("product.ProductParent", on_delete=models.CASCADE, null=True, related_name="product2variantitem") 
    sku = models.CharField(max_length=50)
    quantity = models.IntegerField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    options = models.CharField(max_length=50, null=True, blank=True) # Red/Blue?
    img_upload = models.ImageField(upload_to=path_and_rename, null=True, blank=True, help_text="Primary img")
    img_url = models.CharField(max_length=300, null=True, blank=True, help_text="secondary img") 
    default = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2variantsitem")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return "ParentSn({}) sku({}) Name({}) Options({})".format(self.parent_sn, self.sku, self.name, self.options)


class ProductImage(models.Model):
    id = models.AutoField(primary_key=True)
    parent_sn = models.ForeignKey("product.ProductParent", on_delete=models.CASCADE, null=True, related_name="parent2image") 
    img_upload = models.ImageField(upload_to=path_and_rename, null=True, blank=True, help_text="Primary img")
    img_url = models.CharField(max_length=300, null=True, help_text="Secondary img", blank=True)
    cover_photo = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2img")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 


class ProductVideo(models.Model):
    id = models.AutoField(primary_key=True)
    parent_sn = models.ForeignKey("product.ProductParent", on_delete=models.CASCADE, null=True, related_name="parent2video") 
    video_upload = models.FileField(upload_to=path_and_rename, null=True, blank=True, help_text="Primary file")
    video_url = models.CharField(max_length=250, null=True, blank=True) 
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2video")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 


class ProductTag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2tag")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name


class ProductTagItem(models.Model):
    id = models.AutoField(primary_key=True)
    product_tag = models.ForeignKey("product.ProductTag", on_delete=models.CASCADE, null=True, related_name="tag2items", blank=True) 
    product_variant = models.ForeignKey("product.ProductVariantItem", on_delete=models.CASCADE, null=True, related_name="variant2tag", blank=True) 
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2tagitems")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return "Tag({}) Product({})".format(self.product_tag, self.product_variant)
