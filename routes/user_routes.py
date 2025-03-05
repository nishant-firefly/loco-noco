from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_session
from config.database import DATABASES
from core.repositories.user_repo import UserRepository
from pydantic import BaseModel
from core.models.models import User, Role, EntityRolePermission, RoleToUserMapping
router = APIRouter()

# Request model
class UserCreate(BaseModel):
    first_name: str
    last_name: str | None = None
    username: str
    password: str
    email: str
    is_admin: bool = False

class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    password: str | None = None
    email: str | None = None
    is_admin: bool | None = None

@router.post("/auth/user/registration")
def create_user(user_data: UserCreate, session: Session = Depends(get_session)):
    user_repo = UserRepository(session)
    existing_user = user_repo.get_user_by_email(user_data.email)
    if existing_user:
        return {"error": "User already exists"}
    
    new_user = user_repo.create_user(user_data.dict())
    return new_user

@router.get("/auth/user/{user_id}")
def get_user(user_id: int, session: Session = Depends(get_session)):
    user_repo = UserRepository(session)
    user = user_repo.get(User, user_id)
    if not user:
        return {"error": "User not found"}
    return user


@router.put("/auth/user/{user_id}")
def update_user(user_id: int, user_data: UserUpdate, session: Session = Depends(get_session)):
    user_repo = UserRepository(session)
    updated_user = user_repo.update_user(user_id, user_data.dict(exclude_unset=True))
    return updated_user if updated_user else {"error": "User not found"}

@router.delete("/auth/user/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user_repo = UserRepository(session)
    return {"message": "User deleted successfully"} if user_repo.delete_user(user_id) else {"error": "User not found"}




# from fastapi import APIRouter, Depends
# from fastapi.responses import JSONResponse, PlainTextResponse, Response
# from sqlalchemy.orm import Session
# from config.database import get_session
# from core.repositories.user_repo import UserRepository
# from pydantic import BaseModel
# from core.models.models import User

# router = APIRouter()

# # Request models
# class UserCreate(BaseModel):
#     first_name: str
#     last_name: str | None = None
#     username: str
#     password: str
#     email: str
#     is_admin: bool = False

# class UserUpdate(BaseModel):
#     first_name: str | None = None
#     last_name: str | None = None
#     username: str | None = None
#     password: str | None = None
#     email: str | None = None
#     is_admin: bool | None = None

# @router.post("/auth/user/registration", responses={
#     200: {
#         "content": {
#             "application/json": {"example": {"message": "User created successfully"}},
#             "text/plain": {"example": "User created successfully"},
#             "application/xml": {"example": "<message>User created successfully</message>"}
#         },
#         "description": "Successful Response"
#     }
# })
# def create_user(user_data: UserCreate, session: Session = Depends(get_session), response_type: str = "json"):
#     user_repo = UserRepository(session)
#     existing_user = user_repo.get_user_by_email(user_data.email)
#     if existing_user:
#         return JSONResponse(content={"error": "User already exists"}, status_code=400)
    
#     new_user = user_repo.create_user(user_data.dict())

#     message = "User created successfully"
#     if response_type == "text":
#         return PlainTextResponse(content=message)
#     elif response_type == "xml":
#         return Response(content=f"<message>{message}</message>", media_type="application/xml")
    
#     return JSONResponse(content={"message": message})

# @router.get("/auth/user/{user_id}", responses={
#     200: {
#         "content": {
#             "application/json": {},
#             "text/plain": {},
#             "application/xml": {}
#         },
#         "description": "User Found"
#     },
#     404: {
#         "content": {
#             "application/json": {"example": {"error": "User not found"}},
#             "text/plain": {"example": "User not found"},
#             "application/xml": {"example": "<error>User not found</error>"}
#         },
#         "description": "User Not Found"
#     }
# })
# def get_user(user_id: int, session: Session = Depends(get_session), response_type: str = "json"):
#     user_repo = UserRepository(session)
#     user = user_repo.get(User, user_id)
#     if not user:
#         message = "User not found"
#         if response_type == "text":
#             return PlainTextResponse(content=message, status_code=404)
#         elif response_type == "xml":
#             return Response(content=f"<error>{message}</error>", media_type="application/xml", status_code=404)
#         return JSONResponse(content={"error": message}, status_code=404)
    
#     if response_type == "text":
#         return PlainTextResponse(content=str(user))
#     elif response_type == "xml":
#         return Response(content=f"<user>{user}</user>", media_type="application/xml")
    
#     return JSONResponse(content=user)

# @router.put("/auth/user/{user_id}", responses={
#     200: {
#         "content": {
#             "application/json": {},
#             "text/plain": {},
#             "application/xml": {}
#         },
#         "description": "User Updated"
#     }
# })
# def update_user(user_id: int, user_data: UserUpdate, session: Session = Depends(get_session), response_type: str = "json"):
#     user_repo = UserRepository(session)
#     updated_user = user_repo.update_user(user_id, user_data.dict(exclude_unset=True))
#     if not updated_user:
#         message = "User not found"
#         if response_type == "text":
#             return PlainTextResponse(content=message, status_code=404)
#         elif response_type == "xml":
#             return Response(content=f"<error>{message}</error>", media_type="application/xml", status_code=404)
#         return JSONResponse(content={"error": message}, status_code=404)
    
#     message = "User updated successfully"
#     if response_type == "text":
#         return PlainTextResponse(content=message)
#     elif response_type == "xml":
#         return Response(content=f"<message>{message}</message>", media_type="application/xml")

#     return JSONResponse(content={"message": message})

# @router.delete("/auth/user/{user_id}", responses={
#     200: {
#         "content": {
#             "application/json": {"example": {"message": "User deleted successfully"}},
#             "text/plain": {"example": "User deleted successfully"},
#             "application/xml": {"example": "<message>User deleted successfully</message>"}
#         },
#         "description": "User Deleted"
#     },
#     404: {
#         "content": {
#             "application/json": {"example": {"error": "User not found"}},
#             "text/plain": {"example": "User not found"},
#             "application/xml": {"example": "<error>User not found</error>"}
#         },
#         "description": "User Not Found"
#     }
# })
# def delete_user(user_id: int, session: Session = Depends(get_session), response_type: str = "json"):
#     user_repo = UserRepository(session)
#     if user_repo.delete_user(user_id):
#         message = "User deleted successfully"
#         if response_type == "text":
#             return PlainTextResponse(content=message)
#         elif response_type == "xml":
#             return Response(content=f"<message>{message}</message>", media_type="application/xml")
#         return JSONResponse(content={"message": message})
    
#     message = "User not found"
#     if response_type == "text":
#         return PlainTextResponse(content=message, status_code=404)
#     elif response_type == "xml":
#         return Response(content=f"<error>{message}</error>", media_type="application/xml", status_code=404)
#     return JSONResponse(content={"error": message}, status_code=404)




