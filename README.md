# Telugu Speech Correction App

A real-time speech correction application that helps Telugu speakers improve their English. Speak in Telugu, and the AI will listen, understand, correct you, and respond in English using OpenAI's Realtime API.

## 🎯 Project Overview

This project consists of:
- **Frontend**: React application with real-time audio capture
- **Backend**: FastAPI server that bridges frontend with OpenAI Realtime API
- **AI**: OpenAI's GPT-4 Realtime API for speech-to-speech interaction

## 🏗️ Architecture

```
[User's Microphone] 
      ↓ (Audio Stream)
[React Frontend] 
      ↓ (WebSocket)
[FastAPI Backend] 
      ↓ (WebSocket)
[OpenAI Realtime API]
      ↓ (Response)
[FastAPI Backend]
      ↓ (WebSocket)
[React Frontend]
      ↓ (Audio/Text)
[User Interface]
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (for backend)
- **Node.js 16+** (for frontend)
- **OpenAI API Key** with Realtime API access

### 1. Backend Setup

```bash
# Navigate to backend folder
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Create .env file with your OpenAI API key
# Create a file named .env with the following content:
# OPENAI_API_KEY=sk-your-actual-api-key-here

# Start the backend server
python main.py
```

The backend will start on `http://localhost:8000`

### 2. Frontend Setup

```bash
# Navigate to frontend folder (open a new terminal)
cd frontend

# Install Node dependencies
npm install

# Start the development server
npm run dev
```

The frontend will start on `http://localhost:3000`

### 3. Usage

1. Open your browser and go to `http://localhost:3000`
2. Click **"Connect to Server"**
3. Click **"Start Recording"**
4. Speak in Telugu
5. The AI will listen, correct you, and respond in English
6. View the conversation in real-time on screen

## 📁 Project Structure

```
englishhhhh/
├── backend/
│   ├── main.py              # FastAPI application with WebSocket
│   ├── requirements.txt     # Python dependencies
│   └── README.md           # Backend documentation
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── App.css         # Styling
│   │   ├── main.jsx        # React entry point
│   │   └── index.css       # Global styles
│   ├── index.html          # HTML template
│   ├── vite.config.js      # Vite configuration
│   ├── package.json        # Node dependencies
│   └── README.md          # Frontend documentation
└── README.md              # This file
```

## 🔑 Key Features

### Backend (FastAPI)
- ✅ WebSocket server for real-time communication
- ✅ Direct integration with OpenAI Realtime API
- ✅ Proper system prompt configuration for Telugu to English correction
- ✅ Audio streaming and message forwarding
- ✅ Error handling and logging

### Frontend (React)
- ✅ Real-time audio capture from microphone
- ✅ WebSocket client for backend communication
- ✅ Audio processing (PCM16 format conversion)
- ✅ Live conversation display
- ✅ Modern, responsive UI design
- ✅ Connection status indicators
- ✅ **Audio playback through speakers**
- ✅ **Transcription history with timestamps** - Complete history of Telugu (user) and English (AI) transcriptions
- ✅ **Clear audio buffer** - Manually clear input audio during recording
- ✅ **Real-time transcription display** - See what you and the AI said with timestamps

## 🎓 How It Works

### The Prompt

The AI is configured with this system instruction:

> "You are an English language tutor helping Telugu speakers improve their English. The user will be speaking in Telugu and you have to correct the user and reply in English. Listen carefully to what they say, provide corrections if needed, and respond in clear, proper English. Be encouraging and helpful in your corrections."

### Audio Processing Flow

1. **Capture**: Frontend captures audio from user's microphone
2. **Convert**: Audio is converted to PCM16 format (24kHz, mono)
3. **Encode**: Audio is base64-encoded for transmission
4. **Stream**: Audio chunks are sent via WebSocket to backend
5. **Forward**: Backend forwards audio to OpenAI Realtime API
6. **Process**: OpenAI processes Telugu speech and generates English response
7. **Return**: Response is sent back through the chain
8. **Display**: Frontend displays transcription and plays audio response

## 🛠️ Technologies Used

### Backend
- **FastAPI**: Modern Python web framework
- **WebSockets**: Real-time bidirectional communication
- **OpenAI SDK**: Integration with OpenAI services
- **Uvicorn**: ASGI server

### Frontend
- **React 18**: UI framework
- **Vite**: Fast build tool
- **Web Audio API**: Audio capture and processing
- **WebSocket API**: Real-time communication

## 📝 Configuration

### Backend Configuration

Edit `backend/main.py` to customize:
- System instructions (SYSTEM_INSTRUCTIONS variable)
- OpenAI model settings
- Audio format settings
- Turn detection parameters

### Frontend Configuration

Edit `frontend/src/App.jsx` to customize:
- WebSocket URL (WS_URL constant)
- Audio sample rate
- UI behavior

## 🔒 Security Notes

- **Never commit your `.env` file** with API keys
- Keep your OpenAI API key secure
- Use environment variables for sensitive data
- Consider rate limiting for production deployment

## 🐛 Troubleshooting

### Backend Issues

**"WebSocket error"**
- Verify OpenAI API key is valid
- Check internet connection
- Ensure API key has Realtime API access

**"Connection error"**
- Verify backend is running on port 8000
- Check firewall settings

### Frontend Issues

**"Microphone not working"**
- Grant microphone permissions in browser
- Use HTTPS or localhost
- Check browser compatibility

**"Cannot connect to server"**
- Ensure backend is running
- Verify WebSocket URL is correct
- Check CORS settings

## 📚 Resources

- [OpenAI Realtime API Documentation](https://platform.openai.com/docs/guides/realtime-websocket)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)

## 🚀 Future Enhancements

- [x] Audio playback of AI responses ✅ **IMPLEMENTED**
- [ ] Conversation history persistence
- [ ] User authentication
- [ ] Multiple language support
- [ ] Voice selection
- [ ] Mobile app version
- [ ] Deployment guides (Docker, Cloud)

## 📄 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Feel free to fork, modify, and submit pull requests!

---

**Happy Learning! 🎓** Speak Telugu, Learn English!

