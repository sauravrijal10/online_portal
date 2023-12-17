from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User

class CustomUserAdmin(BaseUserAdmin):
    ordering=['id',]
    list_display = ['id','email','username','first_name','last_name', 'password', 'branch', 'created_at', 'updated_at', 'is_active','is_staff', 'is_admin', 'is_superuser',]
    add_fieldsets = ((None, {'classes': ('wide',),
                             "fields":('email','username','first_name','last_name','password1','password2', 'branch',)}),)
    search_fields =('email',)
admin.site.register(User, CustomUserAdmin)