from django.db import models

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    sku = models.CharField(max_length=50) #Product code
    status = models.IntegerField(null=True) #Product state: 1(normal), 0(abnormal). State of 0, there is no corresponding information
    title = models.CharField(max_length=100, null=True) #Product title
    encrypted_sku = models.CharField(max_length=50, null=True) #Product encrypted code
    color = models.CharField(max_length=10, null=True) #Product color
    size = models.CharField(max_length=5, null=True) #Product size
    ship_weight = models.FloatField(null=True) #	Selling weight(KG)
    volume_weight = models.FloatField(null=True) #Volume weight(KG)
    cat_id = models.IntegerField(null=True) #Category ID
    parent_id = models.IntegerField(null=True) #Parent category ID
    goods_brand = models.CharField(max_length=30, null=True)	 #Product brand
    purchase_title = models.CharField(max_length=100, null=True) #Chinese title
    package_length = models.FloatField(null=True) #Package length
    package_width = models.FloatField(null=True) #Package width
    package_height = models.FloatField(null=True) #Package height
    size_chart = models.CharField(max_length=100, null=True) #	Size table, corresponding to the size chart on the product page of website
    convert_size_chart = models.CharField(max_length=100, null=True) #Size conversion table
    packing_expense = models.FloatField(null=True) #Package expenses
    map = models.TextField(null=True) # array	Minimum Advertised Price. Hereinafter referred to as the MAP
    forbid_platform = models.CharField(max_length=25, null=True) #Prohibited sales platform
    permit_platform = models.CharField(max_length=25, null=True) #Permitted sales platform
    forbid_region = models.CharField(max_length=25, null=True) #Prohibited sales region
    permit_region = models.CharField(max_length=25, null=True) #Permitted sales region
    goods_nature = models.CharField(max_length=5, null=True) #Product attribute ID
    shipping_attributes = models.CharField(max_length=25, null=True) #Product attributes
    original_img = models.TextField(null=True) #	array	Product image url, one-dimensional array
    desc_img = models.TextField(null=True) #	array	Description image url. One-dimensional array
    goods_desc = models.TextField(null=True) #Product description information
    last_update = models.DateField(null=True) #	date	Last updated time(Y-m-d)
    is_amazon_select = models.IntegerField(null=True) #Amazon products or not. 1(yes), 0(no)
    warehouse_list = models.TextField(null=True) #The warehouse in which the product is available for sale.


    def __str__(self):
        return self.sku
