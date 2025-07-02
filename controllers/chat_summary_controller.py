from fastapi import APIRouter
from models.request import ChatSummaryRequest
from services.summarizer import ChatSummarizer
from config import initialize_llm

router = APIRouter()

llm = initialize_llm()
summarizer = ChatSummarizer(llm)

@router.post("/api/chat-summary")
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

