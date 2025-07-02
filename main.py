import os
import uvicorn
from fastapi import FastAPI
from config import setup_environment
from controllers.chat_summary_controller import router as chat_summary_router

# Initialize FastAPI app
app = FastAPI(title="Chat Summary API", description="API to summarize team conversations in Vietnamese")

# Setup environment
setup_environment()

# Include routers
def include_routers(app):
    app.include_router(chat_summary_router)

include_routers(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)