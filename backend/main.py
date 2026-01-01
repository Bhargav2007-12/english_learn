import os
import json
import asyncio
import websockets
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import base64

load_dotenv()

app = FastAPI(title="Telugu Speech Correction API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_REALTIME_URL = "wss://api.openai.com/v1/realtime?model=gpt-realtime"

# System instruction for Telugu to English correction
SYSTEM_INSTRUCTIONS = """You are an English language tutor helping Telugu speakers improve their English. 
The user will be speaking in Telugu and you have to correct the user and reply in English. 
Listen carefully to what they say, provide corrections if needed, and respond in clear, proper English. If they are asking you to say that in telugu because they are not understanding your english, then say in telugu also . 
Be encouraging and helpful in your corrections."""


async def handle_openai_messages(openai_ws, client_ws):
    """Forward messages from OpenAI to client"""
    try:
        async for message in openai_ws:
            print(f"Received from OpenAI: {message}")
            await client_ws.send_text(message)
    except websockets.exceptions.ConnectionClosed:
        print("OpenAI connection closed")
    except Exception as e:
        print(f"Error in OpenAI message handler: {e}")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint that bridges client and OpenAI Realtime API"""
    await websocket.accept()
    print("Client connected")
    
    openai_ws = None
    
    try:
        # Connect to OpenAI Realtime API
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "OpenAI-Beta": "realtime=v1"
        }
        
        openai_ws = await websockets.connect(
            OPENAI_REALTIME_URL,
            extra_headers=headers
        )
        print("Connected to OpenAI Realtime API")
        
        # Send session configuration with system instructions
        session_update = {
            "type": "session.update",
            "session": {
                "modalities": ["text", "audio"],
                "instructions": SYSTEM_INSTRUCTIONS,
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
        }
        await openai_ws.send(json.dumps(session_update))
        print("Session configured with Telugu to English correction prompt")
        
        # Start task to forward OpenAI messages to client
        openai_task = asyncio.create_task(handle_openai_messages(openai_ws, websocket))
        
        # Forward messages from client to OpenAI
        while True:
            try:
                client_message = await websocket.receive_text()
                message_data = json.loads(client_message)
                
                # Log the message type for debugging
                # print(f"Received from client: {client_message}")
                
                # Forward to OpenAI
                await openai_ws.send(client_message)
                
            except WebSocketDisconnect:
                print("Client disconnected")
                break
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                await websocket.send_json({"type": "error", "error": "Invalid JSON"})
            except Exception as e:
                print(f"Error processing client message: {e}")
                break
        
        # Cancel the OpenAI message handler task
        openai_task.cancel()
        try:
            await openai_task
        except asyncio.CancelledError:
            pass
            
    except websockets.exceptions.WebSocketException as e:
        print(f"WebSocket error: {e}")
        await websocket.send_json({"type": "error", "error": str(e)})
    except Exception as e:
        print(f"Unexpected error: {e}")
        await websocket.send_json({"type": "error", "error": str(e)})
    finally:
        if openai_ws:
            await openai_ws.close()
        print("Connection closed")


@app.get("/")
async def root():
    return {
        "message": "Telugu Speech Correction API",
        "status": "running",
        "websocket_endpoint": "/ws"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

