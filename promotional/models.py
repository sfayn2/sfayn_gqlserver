from django.db import models
from django.contrib.auth.models import User
from utils.utils import path_and_rename

# Create your models here.
class PromotionalBanner(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    img_upload = models.ImageField(upload_to=path_and_rename, null=True, blank=True, help_text="Primary img")
    img_url = models.CharField(max_length=300, null=True, blank=True, help_text="secondary img") #TODO imagefield
    display_order = models.PositiveIntegerField(help_text="define order sequence")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2banner")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return "Name({}) Img1({}) Img2({})".format(self.name, self.img_upload, self.img_url)
