import unittest
from auth.services.auth_service import AuthService
from sources.tests.test_config import TEST_ENV_CONFIG


class TestAuthService(unittest.TestCase):
    def setUp(self):
        """
        Dynamically pick the PostgreSQL service configuration and construct the database URL.
        """
        # Retrieve the PostgreSQL service configuration
        postgres_config = TEST_ENV_CONFIG["services"].get("postgres")
        if not postgres_config:
            self.fail("Postgres service configuration is missing in TEST_ENV_CONFIG")

        # Extract host port mapping for PostgreSQL
        host_port = list(postgres_config["ports"].values())[0]
        # Construct the database URL
        self.db_url = f"postgresql://{postgres_config['environment']['POSTGRES_USER']}:" \
                      f"{postgres_config['environment']['POSTGRES_PASSWORD']}@" \
                      f"localhost:{host_port}/" \
                      f"{postgres_config['environment']['POSTGRES_DB']}"
        breakpoint()
        # Initialize the AuthService with the constructed database URL
        self.auth_service = AuthService(self.db_url)


    def test_assign_permission(self):
        """
        Test assigning permissions to a group for an entity.
        """
        group_id = 1
        entity_id = 1
        permissions = {
            "create": True,
            "read": True,
            "update": False,
            "delete": False
        }

        # Call the method to assign permissions
        self.auth_service.assign_permission(group_id, entity_id, permissions)

        # Add assertions based on expected database state
        # Example (if method returns confirmation):
        result = self.auth_service.get_permissions(group_id, entity_id)
        self.assertEqual(result, permissions, "Permissions assigned do not match the expected values")


if __name__ == "__main__":
    unittest.main()
