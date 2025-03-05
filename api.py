from fastapi import FastAPI
from routes.user_routes import router as user_router
from routes.role_routes import router as role_router
from routes.role_to_user_routes import router as role_to_user_router

app = FastAPI(title="Multi DB Query Builder API")

# Include Routes
app.include_router(user_router)
app.include_router(role_router)
app.include_router(role_to_user_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
