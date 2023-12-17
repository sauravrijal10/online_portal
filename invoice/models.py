from django.db import models
from user.models import User

class Invoice(models.Model):
    invoice_created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    remark = models.CharField(max_length=1000)
    created_at =models.DateTimeField(auto_now_add=True,null=False)
    updated_at = models.DateTimeField(auto_now=True,null=False)

    def __str__(self):
        return self.remark
    
    