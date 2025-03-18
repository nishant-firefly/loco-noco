from rest_framework import serializers
from .models import User, Role, EntityRolePermission

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'mobile_number', 'is_email_verified']

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class EntityRolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityRolePermission
        fields = '__all__'



