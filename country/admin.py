from django.contrib import admin
from .models import Country

@admin.register(Country)
class country_list(admin.ModelAdmin):
    list_display = ('id', 'name')
