import os
import uvicorn
from fastapi import FastAPI
from config import setup_environment, initialize_llm
from services.summarizer import ChatSummarizer
from models.request import ChatSummaryRequest

# Initialize FastAPI app
app = FastAPI(title="Chat Summary API", description="API to summarize team conversations in Vietnamese")

# Setup environment and initialize LLM
setup_environment()
llm = initialize_llm()

# Initialize summarizer service
summarizer = ChatSummarizer(llm)

@app.post("/api/chat-summary")
async def chat_summary(request: ChatSummaryRequest):
    """
    Summarize team conversation by fetching messages from .NET server.
    """
    return await summarizer.generate_summary(
        user_id=request.user_id,
        conversation_id=request.conversation_id,
        start_time=request.start_time,
        end_time=request.end_time
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)