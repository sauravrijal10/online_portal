from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone  

from enum import Enum

from branch.models import Branch

from .manager import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField
    first_name = models.CharField(blank=False,null=False,max_length=100)
    last_name = models.CharField(blank=False,null=True,max_length=100)
    email = models.EmailField(blank=False,null=False,max_length=50, unique=True)
    username = models.CharField(blank=True, null=True, max_length=50, unique=True)
    password = models.CharField(blank=False,null=False, max_length=255)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True)
    created_at =models.DateTimeField(auto_now_add=True,null=False)
    updated_at = models.DateTimeField(auto_now=True,null=False)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    
