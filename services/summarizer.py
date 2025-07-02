from fastapi import HTTPException
from langchain_core.prompts import PromptTemplate
from grpc_client import get_chat_messages

class ChatSummarizer:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = PromptTemplate(
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

    async def generate_summary(self, user_id: str, conversation_id: str, start_time: str, end_time: str):
        """Generate summary from chat messages."""
        try:
            messages, date_ranges = await get_chat_messages(user_id, conversation_id, start_time, end_time)
            final_prompt = self.prompt.invoke({"messages": messages, "date_ranges": date_ranges})
            summary = self.llm.invoke(final_prompt.text)
            return {"summary": summary}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi khi tạo tóm tắt: {str(e)}")