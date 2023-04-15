from django.db import models
from django.contrib.auth.models import User

#TODO: to remove 


WAREHOUSE_CHOICES = (
    ("YB",	"CN-1"),
    ("FXQHBSWH",	"CN-2"),
    ("FCYWHQ",	"CN-8"),
    ("FXLAWH",	"US-1"),
    ("FXLAWH2",	"US-2"),
    ("MXTJWH",	"US-3"),
    ("FXJFKGC",	"US-4"),
    ("GBYKDFX",	"UK-3"),
    ("UKCBWH",	"UK-1"),
    ("FXRUWJ",	"RU-2"),
    ("FREDCGC",	"FR-1"),
    ("AU4PXHXY",	"AU-1"),
    ("ESTJWH",	"ES-1"),
    ("FXHKGCZY",	"HK-4"),
    ("ZQ01",	"CN-5"),
    ("ZQDZ01",  "CN-7"),
)


SHIPPING_ATTRIBUTES_CHOICES = (

    (1, "Unlimited"),
    (3, "With Powder"),
    (4, "Self-Defense Weapons"),
    (5, "Fragile"),
    (7,	"Lithium Ion 966"),
    (8,	"Built-In Lithium Ion 967"),
    (9,	"Pure Lithium Ion 965"),
    (10, "Cutting Tools"),
    (11, "Portable Power Source"),
    (12, "High Power Batteries (>100 w)"),
    (13, "Lithium Metal 969"),
    (14, "Pure Lithium Metal 968"),
    (15, "Built-In Lithium Metal 970"),
    (16, "Alkaline Batteries"),
    (17, "With Cream"),
    (18, "With Oily"),
    (19, "With Gas"),
    (20, "With Combustible Solid"),
    (21, "With Colloidal"),
    (22, "With Magnetic"),
    (23, "Imitation Brands"),
    (24, "Imitation Shapes"),
    (25, "Imitation Gun Accessories"),
    (26, "Electronic Cigarette"),
    (27, "Wire Rod"),
    (28, "Memory Device"),
    (29, "With Liquid"),
    (30, "Other Pure Batteries"),
    (31, "Other Built-In Batteries"),
    (32, "Other Matched Batteries"),
    (33, "Nebulizer"),
    (34, "E-Liquid"),
    (35, "MOD"),
    (36, "Vulnerable"),
    (37, "Metal Device"),
    (38, "Laser"),
    (39, "Sex Toys"),
    (40, "Infringing Product"),
    (41, "Sensitive Product"),
    (42, "60CM<=100CM"),
    (43, "100CM<=120CM"),
    (44, "120CM<=150CM"),
    (45, "L>150CM"),
    (46, "Woodiness"),
    (48, "Pure liquid"),
    (52, "With weak magnetic"),
    (53, "Suspected dangerous products"),
    (54, "Medical equipment"),
    (56, "Slingshot"),
    (142, "Built-in lithium ion with mobile power function"),
    (143, "Lead-acid batteries"),
)
# Create your models here.


class ProductCategory(models.Model):
    cat_id = models.PositiveIntegerField(primary_key=True)
    cat_name = models.CharField(max_length=100)
    #parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name="cat2parent", null=True)	#integer	Parent ID.
    parent_id = models.PositiveIntegerField(null=True)	#integer	Parent ID.
    level = models.PositiveIntegerField() #	integer	Category level
    node = models.CharField(max_length=100) #	string	Parent node

    def __str__(self):
        return "parent{}-child{}-cat{}".format(self.parent_id, self.cat_id, self.cat_name)

    class Meta:
        ordering = ("parent_id", "cat_id")


class ProductParent(models.Model):
    parent_sn = models.IntegerField(primary_key=True) #page_result.parent_sn	string	SPU
    #page_result.goods_sn	string	Product code
    is_tort = models.IntegerField() #integer	Whether the product is tort or not. 1 (yes); 0 (no)

class Product(models.Model):
    #id = models.AutoField(primary_key=True)
    sku = models.IntegerField(primary_key=True) #Product code
    parent_sn = models.ForeignKey(ProductParent, null=True, related_name="parent2product", on_delete=models.CASCADE)
    status = models.IntegerField(null=True) #Product state: 1(normal), 0(abnormal). State of 0, there is no corresponding information
    title = models.CharField(max_length=100, null=True) #Product title
    encrypted_sku = models.CharField(max_length=50, null=True) #Product encrypted code
    color = models.CharField(max_length=10, null=True) #Product color
    size = models.CharField(max_length=5, null=True) #Product size
    ship_weight = models.FloatField(null=True) #	Selling weight(KG)
    volume_weight = models.FloatField(null=True) #Volume weight(KG)
    #cat_id = models.IntegerField(null=True) #Category ID
    cat = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, related_name="cat2product") #Category ID
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
        return "sku:{}".format(self.sku)


class ProductWarehouse(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="warehouse")
    url	= models.CharField(max_length=250, null=True) #Product url
    warehouse = models.CharField(max_length=15, null=True, choices=WAREHOUSE_CHOICES) # warehouse in which the product is available for sale
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
    goods_number = models.PositiveIntegerField(null=True) #dunnot why its not in the docs?

    date_created = models.DateTimeField(auto_now_add=True) #added to know when its created (pullpush in sfayn)
    date_modified = models.DateTimeField(auto_now=True) #added to know when its modified 

    def __str__(self):
        return self.warehouse


class ProductMap(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="map")
    map = models.CharField(max_length=50, null=True) #Minimum Advertised Price. Hereinafter referred to as the MAP
    currency = models.CharField(max_length=25, null=True) #Currency for MAP
    limit_price = models.FloatField(null=True) #	float	Price for MAP
    platform = models.CharField(max_length=100, null=True) #	string	Platform for MAP

    date_created = models.DateTimeField(auto_now_add=True) #added to know when its created (pullpush in sfayn)
    date_modified = models.DateTimeField(auto_now=True) #added to know when its modified 


class ProductOriginalImg(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="original_img")
    original_img = models.CharField(max_length=250, null=True) #	array	Product image url, one-dimensional array


class ProductDescImg(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="desc_img")
    desc_img = models.CharField(max_length=250, null=True) #	array	Description image url. One-dimensional array


class ProductStock(models.Model):
    goods_sn = models.ForeignKey(Product, related_name="prod2stock", null=True, on_delete=models.CASCADE) #Product code
    warehouse = models.ForeignKey(ProductWarehouse, related_name="warehouse2stock", null=True, on_delete=models.CASCADE)
    status = models.IntegerField(null=True) #State: 1(stock available); 0(stock unavailable)
    goods_number = models.PositiveIntegerField(null=True) #Available stock
    goods_state = models.CharField(max_length=50, null=True) #	Supply State


class ShoppingCart(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="prod2shopcart")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    quantity = models.IntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True) #added to know when its created (pullpush in sfayn)
    date_modified = models.DateTimeField(auto_now=True) #added to know when its modified 

    class Meta:
        unique_together = ("product", "user")

