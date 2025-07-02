from pydantic import BaseModel

class ChatSummaryRequest(BaseModel):
    user_id: str = ""
    conversation_id: str = ""
    start_time: str  # Format: "DD/MM/YYYY"
    end_time: str    # Format: "DD/MM/YYYY"