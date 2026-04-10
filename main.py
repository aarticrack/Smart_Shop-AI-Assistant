import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router 
from src.core.config import settings

# 1. Initializing the FastAPI App
app = FastAPI(title=settings.PROJECT_NAME)

# 2. Adding CORS Middleware (Essential for Frontend-Backend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Including the routes

app.include_router(router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"status": "SmartShop Backend is Running"}

# 4. The Trigger
if __name__ == "__main__":
    print(f"--- Starting {settings.PROJECT_NAME} on Port 8000 ---")
    # reload=True is great for development, it restarts when you save code
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)