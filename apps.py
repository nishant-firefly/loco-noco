from fastapi import FastAPI
from core.services.options_api import router as options_router

app = FastAPI()

# Include OPTIONS API routes
app.include_router(options_router)

if __name__ == "__apps__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
