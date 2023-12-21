from django.contrib import admin
from .models import Customer_log

@admin.register(Customer_log)
class CustomerLogAdmin(admin.ModelAdmin):
    list_display=('id', 'customer', 'remark','user')