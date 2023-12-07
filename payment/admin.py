from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display=('id','amount','payment_status','payment_source','bank_name','cheque_number','payment_description','payment_creator','payment_type','remark','invoice_id')