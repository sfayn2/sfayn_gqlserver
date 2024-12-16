from django.db import models
from django.contrib.auth.models import User
from utils import path_and_rename

# Create your models here.
class Webhook(models.Model): 

    class Action(models.IntegerChoices):
        CREATE_ORDER = 0
        UPDATE_ORDER_STATUS = 1
        #what else?

    name = models.CharField(max_length=20) #can be outsource?
    url = models.CharField(max_length=200, blank=True, null=True)
    action = models.IntegerField(null=True, choices=Action.choices) 
    secret = models.CharField(max_length=100, blank=True, null=True)
    custom_payload = models.TextField()
    is_active = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2webhook")
    date_created = models.DateTimeField(auto_now_add=True) 
    date_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.name} {self.action}"
