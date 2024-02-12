from django.db import models
from customer.models import Customer
from django.db.models.signals import post_save
from online_portal.middleware import thread_local
from user.models import User
class Customer_log(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    remark = models.CharField(max_length=20000)

