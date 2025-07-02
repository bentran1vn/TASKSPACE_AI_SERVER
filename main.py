from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import os
from datetime import datetime
import uvicorn
from dotenv import load_dotenv
import grpc
import chat_messages_pb2
import chat_messages_pb2_grpc

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Chat Summary API", description="API to summarize team conversations in Vietnamese")


# Pydantic model for request body
class ChatSummaryRequest(BaseModel):
    messages: str
    date_ranges: str


# Function to validate date range format
def validate_date_range(date_range: str) -> bool:
    try:
        start_date, end_date = date_range.split(" - ")
        datetime.strptime(start_date, "%d/%m/%Y")
        datetime.strptime(end_date, "%d/%m/%Y")
        return True
    except ValueError:
        return False


# Set UTF-8 encoding for Vietnamese text
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Check for Google API key
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    print("Error: GOOGLE_API_KEY not found in environment variables.")
    raise Exception("Khóa API Google không được tìm thấy trong biến môi trường.")
else:
    print("GOOGLE_API_KEY loaded successfully.")

# Initialize the model
try:
    llm = GoogleGenerativeAI(model="gemini-1.5-flash-8b", temperature=0.1)
except Exception as e:
    raise Exception(f"Lỗi khi khởi tạo mô hình: {e}")

# Define the prompt template in Vietnamese
prompt = PromptTemplate(
    template="""
Bạn là một trợ lý hữu ích được giao nhiệm vụ tóm tắt cuộc trò chuyện của nhóm để giúp các thành viên mới nhanh chóng nắm bắt thông tin.
Các tin nhắn được định dạng như: "{{username}}: {{nội dung tin nhắn}}".
Cuộc trò chuyện diễn ra từ {date_ranges}.
Hãy tóm tắt cuộc trò chuyện một cách ngắn gọn, tập trung vào các nhiệm vụ chính, thời hạn và quyết định. Bao gồm các ngày hoặc thời gian liên quan nếu được đề cập.
Tránh đưa vào các chi tiết không cần thiết hoặc thông tin trùng lặp.
Tóm tắt phải được viết bằng tiếng Việt.

Tin nhắn:
{messages}

Tóm tắt:
""",
    input_variables=["messages", "date_ranges"],
)


def get_chat_messages_from_dotnet(filter: str) -> tuple[str, str]:
    try:
        # Connect to .NET gRPC server (adjust address as needed)
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = chat_messages_pb2_grpc.ChatMessagesServiceStub(channel)
            request = chat_messages_pb2.ChatMessagesRequest(filter=filter)
            response = stub.GetChatMessages(request)

            if response.error:
                raise Exception(response.error)
            if not response.messages.strip():
                raise Exception("Lỗi: Tin nhắn không được để trống.")
            if not validate_date_range(response.date_ranges):
                raise Exception(
                    "Lỗi: Định dạng khoảng thời gian không hợp lệ. Cần định dạng 'DD/MM/YYYY - DD/MM/YYYY'.")

            return response.messages, response.date_ranges
    except Exception as e:
        raise Exception(f"Lỗi khi gọi .NET server: {str(e)}")

@app.post("/api/chat-summary")
async def chat_summary(request: ChatSummaryRequest):
    """
    Summarize a team conversation in Vietnamese given messages and date range.
    """
    try:
        # Validate inputs
        if not request.messages.strip():
            raise HTTPException(status_code=400, detail="Lỗi: Tin nhắn không được để trống.")
        if not validate_date_range(request.date_ranges):
            raise HTTPException(status_code=400,
                                detail="Lỗi: Định dạng khoảng thời gian không hợp lệ. Cần định dạng 'DD/MM/YYYY - DD/MM/YYYY'.")

        # Format prompt and invoke LLM
        final_prompt = prompt.invoke({"messages": request.messages, "date_ranges": request.date_ranges})
        summary = llm.invoke(final_prompt.text)  # Use .text for GoogleGenerativeAI

        return {"summary": summary}

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi tạo tóm tắt: {str(e)}")


# Run the server (for local testing)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)