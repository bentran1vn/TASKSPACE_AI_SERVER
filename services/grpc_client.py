import grpc
import chat_messages_pb2
import chat_messages_pb2_grpc
from utils.date_validator import validate_date


def get_chat_messages(user_id: str, conversation_id: str, start_time: str, end_time: str) -> tuple[str, str]:
    """
    Fetch chat messages from .NET gRPC server.

    Args:
        user_id: ID of the user to filter messages
        conversation_id: ID of the conversation
        start_time: Start date in DD/MM/YYYY format
        end_time: End date in DD/MM/YYYY format

    Returns:
        Tuple of (messages, date_ranges)

    Raises:
        Exception: If validation fails or server returns an error
    """
    if not (validate_date(start_time) and validate_date(end_time)):
        raise Exception("Lỗi: Định dạng thời gian không hợp lệ. Cần định dạng 'DD/MM/YYYY'.")

    date_ranges = f"{start_time} - {end_time}"

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = chat_messages_pb2_grpc.ChatMessagesServiceStub(channel)
        request = chat_messages_pb2.ChatMessagesRequest(
            user_id=user_id,
            conversation_id=conversation_id,
            start_time=start_time,
            end_time=end_time
        )
        response = stub.GetChatMessages(request)

        if response.error:
            raise Exception(response.error)
        if not response.messages.strip():
            raise Exception("Lỗi: Tin nhắn không được để trống.")

        return response.messages, date_ranges