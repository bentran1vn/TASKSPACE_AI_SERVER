from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
import os


def setup_environment():
    """Load and validate environment variables."""
    load_dotenv()
    os.environ['PYTHONIOENCODING'] = 'utf-8'

    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise Exception("Khóa API Google không được tìm thấy trong biến môi trường.")

    return api_key


def initialize_llm():
    """Initialize and return the language model."""
    try:
        return GoogleGenerativeAI(model="gemini-1.5-flash-8b", temperature=0.1)
    except Exception as e:
        raise Exception(f"Lỗi khi khởi tạo mô hình: {e}")