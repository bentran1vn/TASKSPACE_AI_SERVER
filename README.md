# SummaryBot

An intelligent API service designed to automatically summarize team conversations in Vietnamese using Google's Gemini AI model.

## Overview

SummaryBot processes chat messages retrieved from gRPC server and generates concise, contextually relevant summaries focused on key information such as tasks, deadlines, and decisions. The application is built with FastAPI and designed for serverless deployment on Vercel.

## Key Features

- **Intelligent Summarization**: Utilizes Google's Gemini 1.5 Flash (8B) model to analyze and condense lengthy conversations into clear, actionable summaries in Vietnamese.
- **Date Range Filtering**: Enables users to specify exact date ranges for conversation summaries, allowing targeted information retrieval.
- **API-First Architecture**: Built with FastAPI to provide a responsive, well-documented RESTful API interface.
- **Integration with Existing Systems**: Connects seamlessly with .NET backend services via gRPC.
- **Serverless-Ready**: Optimized for deployment on Vercel's serverless platform.

## Technical Stack

- **Backend Framework**: FastAPI
- **AI/ML**: LangChain with Google Generative AI (Gemini)
- **Communication**: gRPC for service communication
- **Deployment**: Vercel serverless deployment
- **Language**: Python 3.9+

## Project Structure

```
SummaryBot/
├── api/                      # API entry point for Vercel
│   └── index.py              # FastAPI app definition
├── controllers/              # API route controllers
│   └── chat_summary_controller.py
├── models/                   # Data models
│   └── request.py            # Request validation models
├── proto_configs/            # gRPC protocol definitions
│   └── chat_cofig/
│       ├── chat_messages.proto
│       └── generated files
├── services/                 # Business logic
│   ├── grpc_client.py        # gRPC client for chat messages
│   └── summarizer.py         # Summary generation service
├── utils/                    # Utility functions
│   └── date_validator.py     # Date validation utility
├── config.py                 # Configuration and environment setup
├── requirements.txt          # Python dependencies
└── vercel.json               # Vercel deployment configuration
```

## Setup and Installation

### Prerequisites

- Python 3.9+
- Google API key for Gemini model
- A .NET gRPC server with the chat_messages service

### Local Development

1. Clone the repository:
   ```
   git clone <repository-url>
   cd SummaryBot
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with the following variables:
   ```
   GOOGLE_API_KEY=your_google_api_key
   GRPC_HOST=localhost:50051  # Or your gRPC server address
   ```

4. Run the development server:
   ```
   uvicorn api.index:app --reload
   ```

5. Access the API documentation at http://localhost:8000/docs

### Deployment to Vercel

1. Push your code to a Git repository (GitHub, GitLab, or Bitbucket).
2. Connect your repository to Vercel (https://vercel.com/import).
3. Configure environment variables in the Vercel dashboard:
   - `GOOGLE_API_KEY`: Your Google API key
   - `GRPC_HOST`: Your gRPC server address
4. Deploy your project.

## API Usage

### Generate a Summary

```
POST /api/chat-summary

{
  "user_id": "string",
  "conversation_id": "string",
  "start_time": "DD/MM/YYYY",
  "end_time": "DD/MM/YYYY"
}
```

Response:
```json
{
  "summary": "Generated summary text in Vietnamese"
}
```

## License

[MIT License](LICENSE)

## Contributors

- [bentran1vn](https://github.com/bentran1vn)
