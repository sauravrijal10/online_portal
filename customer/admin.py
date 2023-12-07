from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'passport_number','applied_country','branch','file','invoice','contact','status','customer_creator','remark','created_at', 'updated_at')