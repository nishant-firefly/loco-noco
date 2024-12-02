# Core business logic for Auth Module
from sources.rdbms.helpers.rdbms_helper import RDBMSHelper
from auth.models.auth_models import Grouping, UserGrouping, Entity, Permissions

class AuthService:
    def __init__(self, db_url):
        self.helper = RDBMSHelper(db_url)

    def assign_permission(self, group_id, entity_id, permissions):
        """Assign permissions to a group on a specific entity."""
        with self.helper.get_session() as session:
            permission = Permissions(
                grouping_id=group_id,
                entity_id=entity_id,
                permission_json=permissions
            )
            session.add(permission)
