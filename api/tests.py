from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.files.uploadedfile import SimpleUploadedFile
import pandas as pd
import io
import pytest
from django.core.exceptions import ValidationError
from api.models import User, Role, EntityRolePermission
from rest_framework.test import APIClient
from django.contrib.auth.models import User



User = get_user_model()


from rest_framework_simplejwt.tokens import RefreshToken

class UserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="admin", password="adminpass")
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')

    def test_create_user(self):
        data = {"username": "testuser", "password": "testpass", "email": "test@mail.com"}
        response = self.client.post("/api/users/", data)
        # print(response.json())  # Debugging output
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.json())


    def test_get_users(self):
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), list)

    def test_invalid_user_creation(self):
        data = {"username": "", "password": "short"}
        response = self.client.post("/api/users/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.json())

    def test_get_user_detail(self):
        """Test retrieving a specific user by ID."""
        user = User.objects.create_user(username="testuser2", password="testpass")
        response = self.client.get(f"/api/users/{user.id}/")
        
        # Ensure the response is successful and contains user data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["username"], "testuser2")

    def test_delete_user(self):
        """Test deleting a user."""
        user = User.objects.create_user(username="deleteuser", password="testpass")
        response = self.client.delete(f"/api/users/{user.id}/")
        
        # Ensure user deletion was successful
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_user(self):
        """Test updating user information."""
        user = User.objects.create_user(username="updateuser", password="testpass")
        data = {"username": "updatedname", "email": "updated@mail.com"}
        response = self.client.patch(f"/api/users/{user.id}/", data)
        
        # Ensure update was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["username"], "updatedname")


    def test_upload_excel_success(self):
        # Create a sample Excel file in memory
        data = {"Username": ["testuser1", "testuser2"], "Email": ["test1@mail.com", "test2@mail.com"]}
        df = pd.DataFrame(data)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)

        output.seek(0)
        excel_file = SimpleUploadedFile("test.xlsx", output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        response = self.client.post("/api/users/upload_excel/", {"file": excel_file}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_excel_missing_file(self):
        response = self.client.post("/api/users/upload_excel/", {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        """Test user creation with a mobile number"""
        user = User.objects.create(username="testuser", mobile_number="1234567890")
        assert user.username == "testuser"
        assert user.mobile_number == "1234567890"
        assert user.is_email_verified is False
        assert user.is_mobile_verified is False

    def test_mobile_number_unique(self):
        """Test that mobile_number must be unique"""
        User.objects.create(username="user1", mobile_number="1234567890")
        with pytest.raises(Exception):
            User.objects.create(username="user2", mobile_number="1234567890")  # Should fail

    def test_blank_mobile_number(self):
        """Test user creation without a mobile number"""
        user = User.objects.create(username="testuser2")
        assert user.mobile_number is None

@pytest.mark.django_db
class TestRoleModel:
    def test_create_role(self):
        """Test role creation"""
        role = Role.objects.create(name="Admin")
        assert role.name == "Admin"

    def test_unique_role(self):
        """Test that role names must be unique"""
        Role.objects.create(name="Manager")
        with pytest.raises(Exception):
            Role.objects.create(name="Manager")  # Should fail

@pytest.mark.django_db
class TestEntityRolePermissionModel:
    def test_create_entity_role_permission(self):
        """Test permission creation for a role"""
        role = Role.objects.create(name="Editor")
        permission = EntityRolePermission.objects.create(
            role=role, entity_name="Blog", can_create=True, can_read=True
        )
        assert permission.role == role
        assert permission.entity_name == "Blog"
        assert permission.can_create is True
        assert permission.can_read is True
        assert permission.can_update is False
        assert permission.can_delete is False

    def test_role_foreign_key_constraint(self):
        """Test that deleting a Role deletes its permissions"""
        role = Role.objects.create(name="Writer")
        EntityRolePermission.objects.create(role=role, entity_name="Article")
        
        role.delete()  # Deleting the role
        assert EntityRolePermission.objects.count() == 0  

# @pytest.mark.django_db
# def test_some_protected_view():
#     client = APIClient()
#     response = client.get("/some-protected-endpoint/")  # Update with actual URL
#     assert response.status_code == status.HTTP_200_OK
#     assert response.data["message"] == "You have access to this protected endpoint!"




@pytest.mark.django_db
def test_some_protected_view():
    client = APIClient()

    # Create test user
    user = User.objects.create_user(username="postgres", password="postgres")

    # Authenticate the user
    client.force_authenticate(user=user)

    # Make a GET request to the correct URL
    response = client.get("/api/some-protected-endpoint/")  # Adjust this based on your actual API path

    # Validate the response
    assert response.status_code == status.HTTP_200_OK
    assert response.data["message"] == "You have access to this protected endpoint!"

