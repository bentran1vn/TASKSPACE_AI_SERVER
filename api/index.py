import os
from fastapi import FastAPI
from config import setup_environment
from controllers.chat_summary_controller import router as chat_summary_router
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI(title="Chat Summary API", description="API to summarize team conversations in Vietnamese")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup environment
setup_environment()

# Include routers
def include_routers(app):
    app.include_router(chat_summary_router)

include_routers(app)

