from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Zone(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, help_text="ex. Zone 1")
    country = models.CharField(max_length=50, help_text="ex. Singapore")
    region = models.CharField(max_length=50, help_text="ex. Tampines")
    shipping_method = models.ManyToManyField('shipping.Method', related_name="shipmethod2zone", blank=True)
    created_by = models.ForeignKey(
        User, 
        null=True,
        blank=True,
        on_delete=models.CASCADE, 
        related_name="user2zone"
    )
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f'{self.name} {self.country}, {self.region}'


class Classification(models.Model):

    class ClassType(models.IntegerChoices):
        ENTIRE_ORDER = 0
        PER_ITEM = 1

    name = models.CharField(max_length=50, help_text="ex. Heavy Weight")
    desc = models.CharField(max_length=150)

    #AND condition
    # Weight Limit
    min_weight = models.FloatField(null=True, blank=True, help_text="minimum weight of the individual item or all ordered items??")
    max_weight = models.FloatField(null=True, blank=True, help_text="max weight of the individual item or all ordered items??")

    #Package Dimensions LIMIT
    #L+W+H
    min_dimension = models.FloatField(null=True, blank=True, help_text="min package dimension")
    max_dimension = models.FloatField(null=True, blank=True, help_text="max package dimension, should per ordered items??")
    
    cost = models.FloatField(null=True, blank=True, help_text="the cost if condition matched")
    class_type = models.IntegerField(null=True, choices=ClassType.choices, help_text="apply per order or per item?") 
    priority = models.IntegerField(null=True, blank=True, help_text="multiple classification need to have a priority") 

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2classification")
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 


class Method(models.Model):
    id = models.AutoField(primary_key=True)
    #TODO: shipping carrier and duties  & tax??
    #carrier 1 to many?
    #tax 1 to many?
    name = models.CharField(max_length=50, help_text="ex. Free shipping, Local pickup")
    desc = models.CharField(max_length=150)
    classification = models.ManyToManyField('shipping.Classification', related_name="class2shipmethod", blank=True)
    cost = models.FloatField(null=True, blank=True, help_text="cost or overall cost?")
    is_enable = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User, 
        null=True,
        blank=True,
        on_delete=models.CASCADE, 
        related_name="user2method"
    )
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f'{self.title} {self.desc}, {self.cost}'


#class Carrier(models.Model):
#    api?


