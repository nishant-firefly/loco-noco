from fastapi import APIRouter, Response, Depends, HTTPException
from core.services.query_builder import QueryBuilder
from core.models.models import User, Role, EntityRolePermission, RoleToUserMapping
from config.database import DATABASES  # ✅ Import database configurations
from typing import Literal
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from core.repositories.user_repo import UserRepository

router = APIRouter()

# Function to get QueryBuilder for selected database
def get_query_builder(db_type: Literal["postgres", "mysql", "mssql", "oracle"] = "postgres"):
    if db_type not in DATABASES:
        raise ValueError(f"Unsupported database type: {db_type}")
    return QueryBuilder(db_type)

from sqlalchemy.exc import SQLAlchemyError

@router.options("/auth/user/registration/", status_code=200)
async def user_registration_options(response: Response, db_type: str = "postgres"):
    response.headers["Allow"] = "OPTIONS, GET, POST, PUT, DELETE, PATCH"
    response.headers["Content-Type"] = "application/json"

    try:
        query_builder = get_query_builder(db_type)
        users = query_builder.select(User, ["id"]) or []
        total_users = len(users)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return {
        "meta": {"title": "Asharam Management"},
        "form": {
            "title": "Users Registration",
            "form_template": "form-template-one",
            "entity": "/auth/user/registration/",
            "size": {"width": 50, "height": "auto", "maxWidth": 50, "maxHeight": 80},
            "column": {"desktop": 1, "laptop": 1, "tablet": 1},
            "gap": 4,
            "key": "registration"
        },
        "total_users": total_users,
        "permissions": ["get", "put", "patch", "post", "delete", "options"],
        "database": db_type
    }



# CRUD operations for Users
@router.get("/auth/user/registration/")
async def get_users(db_type: str = "postgres"):
    try:
        print(f"Received request with db_type: {db_type}")  # Debugging step 1
        query_builder = get_query_builder(db_type)

        if not query_builder:
            raise HTTPException(status_code=500, detail="Query builder is None")

        print(f"Query Builder Initialized: {query_builder}")  # Debugging step 2

        users = query_builder.select(User)
        print(f"Users Query Executed: {users}")  # Debugging step 3

        return users
    except Exception as e:
        print(f"Error Occurred: {str(e)}")  # Debugging step 4
        raise HTTPException(status_code=500, detail=str(e))




@router.post("/auth/user/registration/")
async def create_user(user: dict, db_type: str = "postgres"):
    query_builder = get_query_builder(db_type)
    return query_builder.insert(User, user)

@router.put("/auth/user/registration/{user_id}")
async def update_user(user_id: int, user: dict, db_type: str = "postgres"):
    query_builder = get_query_builder(db_type)
    return query_builder.update(User, user_id, user)

@router.patch("/auth/user/registration/{user_id}")
async def partial_update_user(user_id: int, user: dict, db_type: str = "postgres"):
    query_builder = get_query_builder(db_type)
    return query_builder.update(User, user_id, user, partial=True)

@router.delete("/auth/user/registration/{user_id}")
async def delete_user(user_id: int, db_type: str = "postgres"):
    query_builder = get_query_builder(db_type)
    return query_builder.delete(User, user_id)



def get_query_builder(db_type: Literal["postgres", "mysql", "mssql", "oracle"] = "postgres"):
    if db_type not in DATABASES:
        raise ValueError(f"Unsupported database type: {db_type}")
    return QueryBuilder(db_type)

# Role Schema
class RoleSchema(BaseModel):
    name: str
    description: str

# OPTIONS - Roles Metadata
@router.options("/api/roles/", status_code=200)
async def roles_options(response: Response):
    response.headers["Allow"] = "OPTIONS, GET, POST, PUT, DELETE, PATCH"
    response.headers["Content-Type"] = "application/json"
    return {
        "meta": {"title": "Asharam Management"},
        "form": {
            "title": "Roles",
            "form_template": "form-template-one",
            "entity": "/api/roles/",
            "size": {"width": 50, "height": "auto", "maxWidth": 50, "maxHeight": 80},
            "key": "roles"
        },
        "permissions": ["get", "put", "patch", "post", "delete", "options"],
    }

# GET - Fetch all roles
@router.get("/api/roles/")
async def get_roles(db_type: str = "postgres"):
    query_builder = get_query_builder(db_type)
    try:
        roles = query_builder.select(Role)
        return {"roles": roles}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# GET - Fetch a specific role by ID
@router.get("/api/roles/{role_id}")
async def get_role(role_id: int, db_type: str = "postgres"):
    query_builder = get_query_builder(db_type)
    role = query_builder.get(Role, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

# POST - Create a new role
@router.post("/api/roles/")
async def create_role(data: RoleSchema, db_type: str = "postgres"):
    query_builder = get_query_builder(db_type)
    new_role = Role(**data.dict())
    try:
        query_builder.insert(new_role)
        return {"message": "Role created successfully", "role": new_role}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# PUT - Replace an existing role
@router.put("/api/roles/{role_id}")
async def update_role(role_id: int, data: RoleSchema, db_type: str = "postgres"):
    query_builder = get_query_builder(db_type)
    existing_role = query_builder.get(Role, role_id)
    if not existing_role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    updated_role = query_builder.update(Role, role_id, data.dict())
    return {"message": "Role updated successfully", "role": updated_role}

# PATCH - Partially update a role
@router.patch("/api/roles/{role_id}")
async def patch_role(role_id: int, data: dict, db_type: str = "postgres"):
    query_builder = get_query_builder(db_type)
    existing_role = query_builder.get(Role, role_id)
    if not existing_role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    patched_role = query_builder.update(Role, role_id, data, partial=True)
    return {"message": "Role patched successfully", "role": patched_role}

# DELETE - Remove a role
@router.delete("/api/roles/{role_id}")
async def delete_role(role_id: int, db_type: str = "postgres"):
    query_builder = get_query_builder(db_type)
    existing_role = query_builder.get(Role, role_id)
    if not existing_role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    query_builder.delete(Role, role_id)
    return {"message": "Role deleted successfully"}


def get_query_builder(db_type: Literal["postgres", "mysql", "mssql", "oracle"] = "postgres"):
    if db_type not in DATABASES:
        raise ValueError(f"Unsupported database type: {db_type}")
    return QueryBuilder(db_type)

# EntityRolePermission Schema
class EntityRolePermissionSchema(BaseModel):
    role_id: int
    entity_id: int
    permission: str

# OPTIONS - Metadata for Entity Role Permissions
@router.options("/api/entity-role-permissions/", status_code=200)
async def entity_role_permissions_options(response: Response):
    response.headers["Allow"] = "OPTIONS, GET, POST, PUT, DELETE, PATCH"
    response.headers["Content-Type"] = "application/json"
    return {
        "meta": {"title": "Asharam Management"},
        "form": {
            "title": "Entity Role Permissions",
            "form_template": "form-template-one",
            "entity": "/api/entity-role-permissions/",
            "size": {"width": 50, "height": "auto", "maxWidth": 50, "maxHeight": 80},
            "key": "entity-role-permissions"
        },
        "permissions": ["get", "put", "patch", "post", "delete", "options"],
    }

# GET - Fetch all entity role permissions
@router.get("/api/entity-role-permissions/")
async def get_entity_role_permissions(db_type: str = "postgres"):
    query_builder = get_query_builder(db_type)
    try:
        permissions = query_builder.select(EntityRolePermission)
        return {"permissions": permissions}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# GET - Fetch a specific entity role permission by ID
@router.get("/api/entity-role-permissions/{permission_id}")
async def get_entity_role_permission(permission_id: int, db_type: str = "postgres"):
    query_builder = get_query_builder(db_type)
    permission = query_builder.get(EntityRolePermission, permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission

# POST - Create a new entity role permission
@router.post("/api/entity-role-permissions/")
async def create_entity_role_permission(data: EntityRolePermissionSchema, db_type: str = "postgres"):
    query_builder = get_query_builder(db_type)
    new_permission = EntityRolePermission(**data.dict())
    try:
        query_builder.insert(new_permission)
        return {"message": "Permission created successfully", "permission": new_permission}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# PUT - Replace an existing entity role permission
@router.put("/api/entity-role-permissions/{permission_id}")
async def update_entity_role_permission(permission_id: int, data: EntityRolePermissionSchema, db_type: str = "postgres"):
    query_builder = get_query_builder(db_type)
    existing_permission = query_builder.get(EntityRolePermission, permission_id)
    if not existing_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    
    updated_permission = query_builder.update(EntityRolePermission, permission_id, data.dict())
    return {"message": "Permission updated successfully", "permission": updated_permission}

# PATCH - Partially update an entity role permission
@router.patch("/api/entity-role-permissions/{permission_id}")
async def patch_entity_role_permission(permission_id: int, data: dict, db_type: str = "postgres"):
    query_builder = get_query_builder(db_type)
    existing_permission = query_builder.get(EntityRolePermission, permission_id)
    if not existing_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    
    patched_permission = query_builder.update(EntityRolePermission, permission_id, data, partial=True)
    return {"message": "Permission patched successfully", "permission": patched_permission}

# DELETE - Remove an entity role permission
@router.delete("/api/entity-role-permissions/{permission_id}")
async def delete_entity_role_permission(permission_id: int, db_type: str = "postgres"):
    query_builder = get_query_builder(db_type)
    existing_permission = query_builder.get(EntityRolePermission, permission_id)
    if not existing_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    
    query_builder.delete(EntityRolePermission, permission_id)
    return {"message": "Permission deleted successfully"}

def get_query_builder(db_type: Literal["postgres", "mysql", "mssql", "oracle"] = "postgres"):
    if db_type not in DATABASES:
        raise ValueError(f"Unsupported database type: {db_type}")
    return QueryBuilder(db_type)

# RoleToUserMapping Schema
class RoleToUserMappingSchema(BaseModel):
    role_id: int
    user_id: int

# OPTIONS - Metadata for Role to User Mapping
@router.options("/api/role-to-user-mapping/", status_code=200)
async def role_to_user_mapping_options(response: Response):
    response.headers["Allow"] = "OPTIONS, GET, POST, PUT, DELETE, PATCH"
    response.headers["Content-Type"] = "application/json"
    return {
        "meta": {"title": "Asharam Management"},
        "form": {
            "title": "Role to User Mapping",
            "form_template": "form-template-one",
            "entity": "/api/role-to-user-mapping/",
            "size": {"width": 50, "height": "auto", "maxWidth": 50, "maxHeight": 80},
            "key": "role-to-user-mapping"
        },
        "permissions": ["get", "put", "patch", "post", "delete", "options"],
    }

# GET - Fetch all role-to-user mappings
@router.get("/api/role-to-user-mapping/")
async def get_role_to_user_mappings(db_type: str = "postgres"):
    query_builder = get_query_builder(db_type)
    try:
        mappings = query_builder.select(RoleToUserMapping)
        return {"role_to_user_mappings": mappings}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# GET - Fetch a specific role-to-user mapping by ID
@router.get("/api/role-to-user-mapping/{mapping_id}")
async def get_role_to_user_mapping(mapping_id: int, db_type: str = "postgres"):
    query_builder = get_query_builder(db_type)
    mapping = query_builder.get(RoleToUserMapping, mapping_id)
    if not mapping:
        raise HTTPException(status_code=404, detail="Mapping not found")
    return mapping

# POST - Create a new role-to-user mapping
@router.post("/api/role-to-user-mapping/")
async def create_role_to_user_mapping(data: RoleToUserMappingSchema, db_type: str = "postgres"):
    query_builder = get_query_builder(db_type)
    new_mapping = RoleToUserMapping(**data.dict())
    try:
        query_builder.insert(new_mapping)
        return {"message": "Mapping created successfully", "mapping": new_mapping}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# PUT - Replace an existing role-to-user mapping
@router.put("/api/role-to-user-mapping/{mapping_id}")
async def update_role_to_user_mapping(mapping_id: int, data: RoleToUserMappingSchema, db_type: str = "postgres"):
    query_builder = get_query_builder(db_type)
    existing_mapping = query_builder.get(RoleToUserMapping, mapping_id)
    if not existing_mapping:
        raise HTTPException(status_code=404, detail="Mapping not found")
    
    updated_mapping = query_builder.update(RoleToUserMapping, mapping_id, data.dict())
    return {"message": "Mapping updated successfully", "mapping": updated_mapping}

# PATCH - Partially update a role-to-user mapping
@router.patch("/api/role-to-user-mapping/{mapping_id}")
async def patch_role_to_user_mapping(mapping_id: int, data: dict, db_type: str = "postgres"):
    query_builder = get_query_builder(db_type)
    existing_mapping = query_builder.get(RoleToUserMapping, mapping_id)
    if not existing_mapping:
        raise HTTPException(status_code=404, detail="Mapping not found")
    
    patched_mapping = query_builder.update(RoleToUserMapping, mapping_id, data, partial=True)
    return {"message": "Mapping patched successfully", "mapping": patched_mapping}

# DELETE - Remove a role-to-user mapping
@router.delete("/api/role-to-user-mapping/{mapping_id}")
async def delete_role_to_user_mapping(mapping_id: int, db_type: str = "postgres"):
    query_builder = get_query_builder(db_type)
    existing_mapping = query_builder.get(RoleToUserMapping, mapping_id)
    if not existing_mapping:
        raise HTTPException(status_code=404, detail="Mapping not found")
    
    query_builder.delete(RoleToUserMapping, mapping_id)
    return {"message": "Mapping deleted successfully"}



# Repeat CRUD operations for Roles, EntityRolePermission, and RoleToUserMapping similarly...
# Add the same pattern of GET, POST, PUT, PATCH, DELETE for these models.







# from fastapi import APIRouter, Response, Depends
# from core.services.query_builder import QueryBuilder
# from core.models.models import User, Role, EntityRolePermission, RoleToUserMapping
# from config.database import DATABASES  # ✅ Import database configurations
# from typing import Literal

# router = APIRouter()

# # Function to get QueryBuilder for selected database
# def get_query_builder(db_type: Literal["postgres", "mysql", "mssql", "oracle"] = "postgres"):
#     if db_type not in DATABASES:
#         raise ValueError(f"Unsupported database type: {db_type}")
#     return QueryBuilder(db_type)

# @router.options("/auth/user/registration/", status_code=200)
# async def user_registration_options(response: Response, db_type: str = "postgres"):
#     response.headers["Allow"] = "OPTIONS, GET, POST, PUT, DELETE, PATCH"
#     response.headers["Content-Type"] = "application/json"

#     query_builder = get_query_builder(db_type)
#     total_users = len(query_builder.select(User, ["id"]))

#     return {
#         "meta": {"title": "Asharam Management"},
#         "form": {
#             "title": "Users Registration",
#             "form_template": "form-template-one",
#             "entity": "/auth/user/registration/",
#             "size": {"width": 50, "height": "auto", "maxWidth": 50, "maxHeight": 80},
#             "column": {"desktop": 1, "laptop": 1, "tablet": 1},
#             "gap": 4,
#             "key": "registration"
#         },
#         "total_users": total_users,
#         "permissions": ["get", "put", "patch", "post", "delete", "options"],
#         "database": db_type
#     }


# @router.options("/api/roles/", status_code=200)
# async def roles_options(response: Response):
#     response.headers["Allow"] = "OPTIONS, GET, POST, PUT, DELETE, PATCH"
#     response.headers["Content-Type"] = "application/json"
#     return {
#         "meta": {"title": "Asharam Management"},
#         "form": {
#             "title": "Roles",
#             "form_template": "form-template-one",
#             "entity": "/api/roles/",
#             "size": {"width": 50, "height": "auto", "maxWidth": 50, "maxHeight": 80},
#             "key": "roles"
#         },
#         "permissions": ["get", "put", "patch", "post", "delete", "options"],
#     }

# @router.options("/api/entity-role-permissions/", status_code=200)
# async def entity_role_permissions_options(response: Response):
#     response.headers["Allow"] = "OPTIONS, GET, POST, PUT, DELETE, PATCH"
#     response.headers["Content-Type"] = "application/json"
#     return {
#         "meta": {"title": "Asharam Management"},
#         "form": {
#             "title": "Entity Role Permissions",
#             "form_template": "form-template-one",
#             "entity": "/api/entity-role-permissions/",
#             "size": {"width": 50, "height": "auto", "maxWidth": 50, "maxHeight": 80},
#             "key": "entity-role-permissions"
#         },
#         "permissions": ["get", "put", "patch", "post", "delete", "options"],
    # }

# @router.options("/api/role-to-user-mapping/", status_code=200)
# async def role_to_user_mapping_options(response: Response):
#     response.headers["Allow"] = "OPTIONS, GET, POST, PUT, DELETE, PATCH"
#     response.headers["Content-Type"] = "application/json"
#     return {
#         "meta": {"title": "Asharam Management"},
#         "form": {
#             "title": "Role to User Mapping",
#             "form_template": "form-template-one",
#             "entity": "/api/role-to-user-mapping/",
#             "size": {"width": 50, "height": "auto", "maxWidth": 50, "maxHeight": 80},
#             "key": "role-to-user-mapping"
#         },
#         "permissions": ["get", "put", "patch", "post", "delete", "options"],
#     }
























# from fastapi import APIRouter, Response

# router = APIRouter()

# @router.options("/auth/user/registration/", status_code=200)
# async def user_registration_options(response: Response):
#     response.headers["Allow"] = "OPTIONS, GET, POST, PUT, DELETE, PATCH"
#     response.headers["Content-Type"] = "application/json"
#     return {
#         "meta": {"title": "Asharam Management"},
#         "form": {
#             "title": "Users Registration",
#             "form_template": "form-template-one",
#             "entity": "/auth/user/registration/",
#             "size": {"width": 50, "height": "auto", "maxWidth": 50, "maxHeight": 80},
#             "column": {"desktop": 1, "laptop": 1, "tablet": 1},
#             "gap": 4,
#             "key": "registration"
#         },
#         "permissions": ["get", "put", "patch", "post", "delete", "options"],
#     }

# @router.options("/api/roles/", status_code=200)
# async def roles_options(response: Response):
#     response.headers["Allow"] = "OPTIONS, GET, POST, PUT, DELETE, PATCH"
#     response.headers["Content-Type"] = "application/json"
#     return {
#         "meta": {"title": "Asharam Management"},
#         "form": {
#             "title": "Roles",
#             "form_template": "form-template-one",
#             "entity": "/api/roles/",
#             "size": {"width": 50, "height": "auto", "maxWidth": 50, "maxHeight": 80},
#             "key": "roles"
#         },
#         "permissions": ["get", "put", "patch", "post", "delete", "options"],
#     }

# @router.options("/api/entity-role-permissions/", status_code=200)
# async def entity_role_permissions_options(response: Response):
#     response.headers["Allow"] = "OPTIONS, GET, POST, PUT, DELETE, PATCH"
#     response.headers["Content-Type"] = "application/json"
#     return {
#         "meta": {"title": "Asharam Management"},
#         "form": {
#             "title": "Entity Role Permissions",
#             "form_template": "form-template-one",
#             "entity": "/api/entity-role-permissions/",
#             "size": {"width": 50, "height": "auto", "maxWidth": 50, "maxHeight": 80},
#             "key": "entity-role-permissions"
#         },
#         "permissions": ["get", "put", "patch", "post", "delete", "options"],
#     }

# @router.options("/api/role-to-user-mapping/", status_code=200)
# async def role_to_user_mapping_options(response: Response):
#     response.headers["Allow"] = "OPTIONS, GET, POST, PUT, DELETE, PATCH"
#     response.headers["Content-Type"] = "application/json"
#     return {
#         "meta": {"title": "Asharam Management"},
#         "form": {
#             "title": "Role to User Mapping",
#             "form_template": "form-template-one",
#             "entity": "/api/role-to-user-mapping/",
#             "size": {"width": 50, "height": "auto", "maxWidth": 50, "maxHeight": 80},
#             "key": "role-to-user-mapping"
#         },
#         "permissions": ["get", "put", "patch", "post", "delete", "options"],
#     }
