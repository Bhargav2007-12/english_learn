# System Architecture

## Overview

This application enables real-time Telugu to English speech correction using OpenAI's Realtime API through a FastAPI backend and React frontend.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                │
│                    (Telugu Speaker)                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Speaks Telugu
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   REACT FRONTEND                            │
│                  (localhost:3000)                           │
│                                                             │
│  ┌───────────────────────────────────────────────────┐    │
│  │  Audio Capture (Web Audio API)                    │    │
│  │  • Microphone input                               │    │
│  │  • PCM16 conversion (24kHz, mono)                 │    │
│  │  • Base64 encoding                                │    │
│  └───────────────────────────────────────────────────┘    │
│                          │                                  │
│  ┌───────────────────────────────────────────────────┐    │
│  │  WebSocket Client                                 │    │
│  │  • Sends audio chunks                             │    │
│  │  • Receives responses                             │    │
│  │  • Displays conversation                          │    │
│  └───────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ WebSocket
                            │ ws://localhost:8000/ws
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  FASTAPI BACKEND                            │
│                  (localhost:8000)                           │
│                                                             │
│  ┌───────────────────────────────────────────────────┐    │
│  │  WebSocket Server (/ws endpoint)                  │    │
│  │  • Accepts client connections                     │    │
│  │  • Bidirectional message forwarding               │    │
│  └───────────────────────────────────────────────────┘    │
│                          │                                  │
│  ┌───────────────────────────────────────────────────┐    │
│  │  OpenAI Integration                               │    │
│  │  • Establishes WebSocket to OpenAI                │    │
│  │  • Configures session with prompt                 │    │
│  │  • Forwards audio and messages                    │    │
│  └───────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ WebSocket
                            │ wss://api.openai.com/v1/realtime
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              OPENAI REALTIME API                            │
│              (GPT-4 Realtime Preview)                       │
│                                                             │
│  ┌───────────────────────────────────────────────────┐    │
│  │  Speech Recognition                               │    │
│  │  • Transcribes Telugu audio                       │    │
│  │  • Understands context                            │    │
│  └───────────────────────────────────────────────────┘    │
│                          │                                  │
│  ┌───────────────────────────────────────────────────┐    │
│  │  Language Processing                              │    │
│  │  • Analyzes Telugu speech                         │    │
│  │  • Identifies errors/corrections needed           │    │
│  │  • Generates English response                     │    │
│  └───────────────────────────────────────────────────┘    │
│                          │                                  │
│  ┌───────────────────────────────────────────────────┐    │
│  │  Response Generation                              │    │
│  │  • Text transcript                                │    │
│  │  • Audio synthesis (English)                      │    │
│  └───────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Response
                            ▼
                    [Back through stack]
                            │
                            ▼
                         USER
                   (Hears/Reads English)
```

## Data Flow

### 1. Audio Capture (Frontend)

```javascript
User speaks → Microphone → Web Audio API → 
AudioContext (24kHz) → ScriptProcessor → 
Float32Array → Int16Array (PCM16) → 
Base64 encoding → WebSocket message
```

### 2. WebSocket Message Format

**Sending Audio:**
```json
{
  "type": "input_audio_buffer.append",
  "audio": "base64_encoded_pcm16_data"
}
```

**Receiving Transcription:**
```json
{
  "type": "conversation.item.created",
  "item": {
    "content": [
      {"transcript": "User's Telugu speech transcribed"}
    ]
  }
}
```

**Receiving Response:**
```json
{
  "type": "response.audio_transcript.delta",
  "delta": "AI's English response text..."
}
```

### 3. Backend Processing

```
Frontend WebSocket → 
FastAPI endpoint handler →
OpenAI WebSocket connection →
Message forwarding (bidirectional) →
Error handling & logging
```

### 4. OpenAI Processing

```
Audio buffer → 
Speech recognition (Telugu) →
GPT-4 processing with system prompt →
English response generation →
Audio synthesis (optional) →
Response streaming
```

## Key Components

### Frontend (React)

**Files:**
- `App.jsx` - Main component with WebSocket and audio logic
- `App.css` - Styling and UI design
- `main.jsx` - React entry point
- `index.css` - Global styles

**Technologies:**
- Web Audio API
- WebSocket API
- React Hooks (useState, useRef, useEffect)

### Backend (FastAPI)

**Files:**
- `main.py` - FastAPI app with WebSocket server
- `requirements.txt` - Python dependencies

**Technologies:**
- FastAPI
- WebSockets library
- Asyncio for concurrent operations

### System Prompt

The critical instruction that makes this work:

```
You are an English language tutor helping Telugu speakers 
improve their English. The user will be speaking in Telugu 
and you have to correct the user and reply in English. 
Listen carefully to what they say, provide corrections if 
needed, and respond in clear, proper English. Be encouraging 
and helpful in your corrections.
```

## Configuration Details

### Audio Settings

| Parameter | Value | Purpose |
|-----------|-------|---------|
| Sample Rate | 24000 Hz | OpenAI Realtime API requirement |
| Channels | 1 (Mono) | Simplified processing |
| Format | PCM16 | 16-bit signed integer |
| Encoding | Base64 | WebSocket transmission |
| Buffer Size | 4096 samples | Balanced latency/quality |

### Session Configuration

```json
{
  "modalities": ["text", "audio"],
  "instructions": "<system_prompt>",
  "voice": "alloy",
  "input_audio_format": "pcm16",
  "output_audio_format": "pcm16",
  "input_audio_transcription": {
    "model": "whisper-1"
  },
  "turn_detection": {
    "type": "server_vad",
    "threshold": 0.5,
    "prefix_padding_ms": 300,
    "silence_duration_ms": 500
  },
  "temperature": 0.8,
  "max_response_output_tokens": 4096
}
```

## Security Considerations

1. **API Key Protection**
   - Stored in `.env` file (backend only)
   - Never exposed to frontend
   - Added to `.gitignore`

2. **CORS Configuration**
   - Restricted to localhost origins
   - Configured in FastAPI backend

3. **WebSocket Security**
   - OpenAI connection uses WSS (secure)
   - Local connections use WS (development only)

4. **Data Privacy**
   - Audio streamed, not stored
   - No conversation persistence (by default)

## Scalability Considerations

### Current Architecture (Development)

- Single server instance
- No load balancing
- No session persistence
- Localhost only

### Production Considerations (Future)

- Multiple backend instances
- Load balancer (nginx/Cloudflare)
- Redis for session management
- HTTPS/WSS everywhere
- Rate limiting
- User authentication
- Conversation storage (database)
- CDN for frontend assets

## Performance Characteristics

### Latency Breakdown

1. **Audio capture to frontend send**: ~100ms
2. **WebSocket to backend**: ~1-5ms (localhost)
3. **Backend to OpenAI**: ~10-50ms (network)
4. **OpenAI processing**: ~500-2000ms (AI inference)
5. **Response back**: ~100ms
6. **Total**: ~1-3 seconds typical

### Optimization Opportunities

- Reduce audio buffer size (lower latency, higher CPU)
- Use audio delta streaming for playback
- Implement client-side audio preprocessing
- Add connection pooling
- Cache common responses

## Error Handling

### Frontend
- WebSocket connection failures
- Microphone access denial
- Audio processing errors
- Network interruptions

### Backend
- OpenAI API failures
- WebSocket disconnections
- Invalid message formats
- Authentication errors

### Recovery Strategies
- Automatic reconnection attempts
- User-friendly error messages
- Graceful degradation
- Connection state management

## Testing Strategy

### Manual Testing
1. Connection establishment
2. Audio capture functionality
3. Speech recognition accuracy
4. Response quality
5. Error scenarios

### Automated Testing (Future)
- Unit tests for audio processing
- Integration tests for WebSocket flow
- End-to-end tests with mock OpenAI
- Performance/load testing

## Deployment Architecture (Future)

```
[Users] → [CDN/Static Host (Frontend)] → 
[Load Balancer] → [FastAPI Instances] → 
[OpenAI Realtime API]
         ↓
    [Database]
    [Redis Cache]
```

## Resources & References

- [OpenAI Realtime API Docs](https://platform.openai.com/docs/guides/realtime-websocket)
- [FastAPI WebSocket Guide](https://fastapi.tiangolo.com/advanced/websockets/)
- [Web Audio API MDN](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)
- [React Hooks Reference](https://react.dev/reference/react)

---

**Note**: This architecture is designed for development and demonstration. Production deployment would require additional security, scalability, and reliability measures.

