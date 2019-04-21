from django.db import models

# Create your models here.
class Product(models.Model):
    #id = models.AutoField(primary_key=True)
    sku = models.CharField(max_length=50, primary_key=True) #Product code
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
    #map = models.TextField(null=True) # array	Minimum Advertised Price. Hereinafter referred to as the MAP
    forbid_platform = models.CharField(max_length=25, null=True) #Prohibited sales platform
    permit_platform = models.CharField(max_length=25, null=True) #Permitted sales platform
    forbid_region = models.CharField(max_length=25, null=True) #Prohibited sales region
    permit_region = models.CharField(max_length=25, null=True) #Permitted sales region
    goods_nature = models.CharField(max_length=5, null=True) #Product attribute ID
    shipping_attributes = models.CharField(max_length=25, null=True) #Product attributes
    #original_img = models.TextField(null=True) #	array	Product image url, one-dimensional array
    #desc_img = models.TextField(null=True) #	array	Description image url. One-dimensional array
    goods_desc = models.TextField(null=True) #Product description information
    last_update = models.DateField(null=True) #	date	Last updated time(Y-m-d)
    is_amazon_select = models.IntegerField(null=True) #Amazon products or not. 1(yes), 0(no)
    
    video_url = models.CharField(max_length=50, null=True) #not in the docs but in the API results?
    hs_code = models.CharField(max_length=50, null=True) #not in the docs but in the API results?

    date_created = models.DateTimeField(auto_now_add=True) #added to know when its created (pullpush in sfayn)
    date_modified = models.DateTimeField(auto_now=True) #added to know when its modified 


    def __str__(self):
        return self.sku


class ProductWarehouse(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="warehouse")
    url	= models.CharField(max_length=250, null=True) #Product url
    warehouse = models.CharField(max_length=15, null=True) # warehouse in which the product is available for sale
    price = models.FloatField(null=True) # Product Price(USD)
    is_clearance = models.IntegerField(null=True)	 #Product clearance or not: 1(yes); 0(no)
    clearance_price = models.FloatField(null=True) #Clearance price. Only for the clearance product
    is_promote = models.IntegerField(null=True) #Product promotion or not: 1(yes); 0(no)
    promote_price = models.FloatField(null=True) #Promotion price. Only for the promotion product
    promote_cancel_time	= models.CharField(max_length=100, null=True) #取消促销时间，是促销品才有这个时间，为0表示正在促销，大于0表示在这个时间之后就会自动取消促销
    is_new = models.IntegerField(null=True) # 是否新品：1(是)；0(否)
    new_price = models.FloatField(null=True) # 新品价格，是新品才有这个价格
    new_stock = models.IntegerField(null=True) # 新品剩余库存，是新品才有这个字段
    new_stock_total = models.IntegerField(null=True) #	新品总库存，是新品才有这个字段
    handling_fee = models.FloatField(null=True) # Handling fee
    sale_time = models.DateField(null=True) #	Listing time(Y-m-d)
    goods_state = models.CharField(max_length=50, null=True) #	Supply State
    purchase_info = models.CharField(max_length=400, null=True) #	array	In-transit inventory information

    date_created = models.DateTimeField(auto_now_add=True) #added to know when its created (pullpush in sfayn)
    date_modified = models.DateTimeField(auto_now=True) #added to know when its modified 

    def __str__(self):
        return self.warehouse


class ProductMap(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="map")
    map = models.CharField(max_length=50, null=True) #Minimum Advertised Price. Hereinafter referred to as the MAP
    currency = models.CharField(max_length=25, null=True) #Currency for MAP
    limit_price = models.FloatField(null=True) #	float	Price for MAP
    platform = models.CharField(max_length=100, null=True) #	string	Platform for MAP

    date_created = models.DateTimeField(auto_now_add=True) #added to know when its created (pullpush in sfayn)
    date_modified = models.DateTimeField(auto_now=True) #added to know when its modified 


class ProductOriginalImg(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="original_img")
    original_img = models.CharField(max_length=250, null=True) #	array	Product image url, one-dimensional array


class ProductDescImg(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="desc_img")
    desc_img = models.CharField(max_length=250, null=True) #	array	Description image url. One-dimensional array
