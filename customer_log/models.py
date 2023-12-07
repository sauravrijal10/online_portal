from django.db import models
from customer.models import Customer

class Customer_log(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    remark = models.CharField(max_length=20000)

    def __str__(self):
        return self.customer_id.name