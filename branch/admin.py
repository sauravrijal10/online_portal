from django.contrib import admin
from .models import Branch

@admin.register(Branch)
class branch_list(admin.ModelAdmin):
    list_display = ('id', 'name','country','mobile','telephone','cr','email','website','logo')