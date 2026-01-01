# Telugu Speech Correction Backend

FastAPI backend that bridges the React frontend with OpenAI's Realtime API for Telugu to English speech correction.

## Setup

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure environment variables:**
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to `.env`:
     ```
     OPENAI_API_KEY=sk-your-actual-api-key-here
     ```

3. **Run the server:**
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will start on `http://localhost:8000`

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `WebSocket /ws` - Main WebSocket endpoint for real-time audio streaming

## How It Works

1. Frontend connects to `/ws` WebSocket endpoint
2. Backend establishes connection to OpenAI Realtime API
3. Audio and messages are bidirectionally streamed:
   - Client audio → Backend → OpenAI Realtime API
   - OpenAI responses → Backend → Client
4. The system is configured with instructions to:
   - Listen to Telugu speech
   - Provide corrections
   - Respond in English

## WebSocket Message Format

The backend forwards messages between the client and OpenAI's Realtime API. See OpenAI's documentation for message formats:
https://platform.openai.com/docs/guides/realtime-websocket

Common message types:
- `session.update` - Configure the session
- `input_audio_buffer.append` - Send audio data
- `response.create` - Request a response
- `conversation.item.create` - Add conversation items

## Requirements

- Python 3.8+
- OpenAI API key with access to Realtime API
- Active internet connection

