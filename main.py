from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_session
from core.repositories.user_repo import UserRepository
from core.models.models import User, Role, EntityRolePermission, RoleToUserMapping
from pydantic import BaseModel, EmailStr
from typing import Optional
from config.logger import logger

app = FastAPI()

# Dependency to get DB session
def get_db():
    session = get_session("postgres")  # Change to "mysql", "mssql", "oracle" as needed
    try:
        yield session
    finally:
        session.close()

# Pydantic model for request validation
class UserCreate(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    password: str
    email: EmailStr
    is_admin: bool = False

@app.post("/auth/user/registration/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    new_user = user_repo.create(User, user.dict())
    
    if not new_user:
        raise HTTPException(status_code=400, detail="User creation failed")

    return {"id": new_user.id, "first_name": new_user.first_name, "email": new_user.email}

@app.get("/auth/user/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    user = user_repo.get(User, user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"id": user.id, "first_name": user.first_name, "email": user.email}

@app.put("/auth/user/{user_id}")
def update_user(user_id: int, user_data: UserCreate, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    updated_user = user_repo.update(User, user_id, user_data.dict())
    
    if not updated_user:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"id": updated_user.id, "first_name": updated_user.first_name, "email": updated_user.email}

@app.delete("/auth/user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    deleted = user_repo.delete(User, user_id)
    
    if not deleted:
        raise HTTPException(status_code=400, detail="Delete failed")

    return {"message": "User deleted successfully"}





# from config.database import get_session
# from core.repositories.user_repo import UserRepository
# from core.models.user import User
# from config.logger import logger

# logger.info("Starting the application...")


# db_type = "postgres"  # Change this to "mysql", "mssql", "oracle" as needed
# session = get_session(db_type)
# user_repo = UserRepository(session)

# # CREATE
# new_user = user_repo.create(User, {"name": "John Doe", "email": "john@example.com"})
# print(f"User Created: {new_user.id}, {new_user.name}, {new_user.email}")

# # READ
# retrieved_user = user_repo.get(User, new_user.id)
# print(f"User Retrieved: {retrieved_user.id}, {retrieved_user.name}, {retrieved_user.email}")

# # UPDATE
# updated_user = user_repo.update(User, new_user.id, {"name": "John Smith"})
# print(f"User Updated: {updated_user.id}, {updated_user.name}, {updated_user.email}")

# # DELETE
# deleted = user_repo.delete(User, new_user.id)
# print(f"User Deleted: {deleted}")
