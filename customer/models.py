from django.db import models
from branch.models import Branch
from user.models import User
from invoice.models import Invoice
from enum import Enum


class Customer(models.Model):
    class status_types(Enum):
        REFUNDED = "REFUNDED"
        PROCESSING_CANCELLED = "PROCESSING_CANCELLED"
        VISA_REJECTED = "VISA_REJECTED"
        VISA_SUCCESS = "VISA_SUCCESS"
        PASSPORT_SUBMITED_ON_EMBASSY = "PASSPORT_SUBMITED_ON_EMBASSY"
        PERMIT_RECEIVED = "PERMIT_RECEIVED"
        SUBMISSION_RECEIVED = "SUBMISSION_RECEIVED"
        APPLIED = "APPLIED"
    name = models.CharField(max_length=255)
    passport_number = models.CharField(max_length=255)
    applied_country = models.CharField(max_length=255)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE, blank=True, null=True)
    file = models.CharField(max_length=10000, blank=True, null=True)
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE, null=True, blank=True)
    contact = models.CharField(max_length=255)
    status = models.CharField(choices=((x.value,x.name.title()) for x in status_types),null=False,max_length=50,blank=False,default=status_types.APPLIED.value,)
    customer_creator = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True)
    remark = models.CharField(max_length=1000)
    created_at =models.DateTimeField(auto_now_add=True,null=False)
    updated_at = models.DateTimeField(auto_now=True,null=False)

    
    def __str__(self):
        return self.name
    