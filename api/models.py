from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    mobile_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    is_mobile_verified = models.BooleanField(default=False)

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

class EntityRolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    entity_name = models.CharField(max_length=100)
    can_create = models.BooleanField(default=False)
    can_read = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
