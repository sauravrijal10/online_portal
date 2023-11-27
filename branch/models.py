from django.db import models
from country.models import Country

class Branch(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=255)
    telephone = models.CharField(max_length=255)
    cr = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    website = models.CharField(max_length=255)
    logo = models.CharField(max_length=255)

    def __str__(self):
        return self.name