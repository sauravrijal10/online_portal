from django.db import models
# from user.models import User
from django.contrib.auth import get_user_model


class Country(models.Model):
    name = models.CharField(max_length=255)
    currency = models.CharField(max_length=255, blank=True, null=True)
    # added_by = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True)
    added_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name