from django.db import models
from enum import Enum
from user.models import User
from invoice.models import Invoice



class Payment(models.Model):
    class status(Enum):
        COMPLETED = "COMPLETED"
        INCOMPLETE = "INCOMPLETE"
    class source(Enum):
        CASH = "CASH"
        BANK_TRANSFER = "BANK_TRANSFER"
        CHEQUE = "CHEQUE"
    class PaymentType(Enum):
        FIRST = "FIRST"
        SECOND = "SECOND"
        THIRD = "THIRD"
    amount = models.BigIntegerField()
    payment_status = models.CharField(choices=((x.value,x.name.title()) for x in status),null=False,max_length=50,blank=False)
    payment_source = models.CharField(choices=((x.value,x.name.title()) for x in source),null=False,max_length=50,blank=False)
    bank_name = models.CharField(max_length=255,null=True,blank=True)
    cheque_number = models.CharField(max_length=255, null=True,blank=True)
    payment_description = models.CharField(max_length=1000)
    payment_creator = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    payment_type = models.CharField(choices=((x.value,x.name.title()) for x in PaymentType),null=False,max_length=50,blank=False)
    remark = models.CharField(max_length=1000)
    invoice_id = models.ForeignKey(Invoice, on_delete=models.CASCADE)

