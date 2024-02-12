from django.db import models
from django.apps import apps
# from django.contrib.auth import get_user_model


class Branch(models.Model):
    name = models.CharField(max_length=251)
    country = models.ForeignKey('country.Country', on_delete=models.CASCADE)
    city = models.CharField(max_length=255,null=True)
    mobile = models.CharField(max_length=255)
    telephone = models.CharField(max_length=255, blank=True, null=True)
    cr = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, unique=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    logo = models.CharField(max_length=255, blank=True, null=True)
    # added_by = models.ForeignKey('user.User', on_delete=models.CASCADE, blank=True, null=True)

    

    def __str__(self):
        return self.name