# Setup Instructions

Follow these steps to get the Telugu Speech Correction app running on your machine.

## Prerequisites

Before you begin, ensure you have:

1. **Python 3.8 or higher** installed
   - Check: `python --version` or `python3 --version`
   - Download: https://www.python.org/downloads/

2. **Node.js 16 or higher** installed
   - Check: `node --version`
   - Download: https://nodejs.org/

3. **OpenAI API Key** with Realtime API access
   - Get one at: https://platform.openai.com/api-keys
   - Note: Realtime API may require a paid account

## Step-by-Step Setup

### Step 1: Configure Backend

Open a terminal and navigate to the backend folder:

```bash
cd backend
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Create your `.env` file with your OpenAI API key:

**On Windows (PowerShell):**
```powershell
Copy-Item .env.template .env
notepad .env
```

**On Mac/Linux:**
```bash
cp .env.template .env
nano .env
```

Edit the `.env` file and replace `sk-your-openai-api-key-here` with your actual OpenAI API key.

### Step 2: Start Backend Server

While still in the `backend` folder:

```bash
python main.py
```

You should see output like:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ **Keep this terminal window open!** The backend needs to stay running.

### Step 3: Configure Frontend

Open a **NEW terminal window** and navigate to the frontend folder:

```bash
cd frontend
```

Install Node.js dependencies:

```bash
npm install
```

This will download all required packages. It may take a few minutes.

### Step 4: Start Frontend

While still in the `frontend` folder:

```bash
npm run dev
```

You should see output like:
```
  VITE v5.0.0  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

### Step 5: Open the App

Open your web browser and go to:

```
http://localhost:3000
```

### Step 6: Test the Application

1. Click **"Connect to Server"** button
   - Status should change to 🟢 Connected

2. Click **"Start Recording"** button
   - You'll be prompted to allow microphone access - click "Allow"
   - The app will show 🔴 Recording...

3. **Speak in Telugu!**
   - The AI will listen and understand
   - It will provide corrections and respond in English

4. Watch the conversation panel for:
   - Your transcribed speech
   - AI's corrections and responses
   - System messages

## Troubleshooting

### Backend Won't Start

**Error: "No module named 'fastapi'"**
- Solution: Install dependencies with `pip install -r requirements.txt`

**Error: "OPENAI_API_KEY not found"**
- Solution: Ensure `.env` file exists in `backend/` folder with your API key

**Error: "Port 8000 is already in use"**
- Solution: Stop any other programs using port 8000, or edit `main.py` to use a different port

### Frontend Won't Start

**Error: "Cannot find module"**
- Solution: Run `npm install` in the frontend folder

**Error: "Port 3000 is already in use"**
- Solution: The terminal will ask if you want to use a different port - press 'y'

### Connection Issues

**"Cannot connect to server"**
- Ensure backend is running (check terminal)
- Verify backend URL in `frontend/src/App.jsx` is `ws://localhost:8000/ws`

**Microphone not working**
- Grant microphone permissions when browser asks
- Check your system microphone settings
- Try refreshing the page

### API Issues

**"OpenAI connection failed"**
- Verify your API key is valid
- Ensure you have Realtime API access (may require paid plan)
- Check your internet connection

## What's Next?

Once everything is running:

1. Test with simple Telugu phrases
2. Listen to the AI's English corrections
3. Try different types of conversations
4. Explore the code to customize the behavior!

## Getting Help

If you encounter issues:

1. Check the terminal outputs for error messages
2. Review the main README.md for detailed documentation
3. Consult the troubleshooting sections in:
   - `backend/README.md`
   - `frontend/README.md`

## Stopping the Application

To stop the servers:

1. In each terminal window, press `Ctrl+C` (Windows/Linux) or `Cmd+C` (Mac)
2. This will gracefully shut down the servers

## Next Steps

Want to customize the app? Check out:

- Backend prompt customization: `backend/main.py` (SYSTEM_INSTRUCTIONS)
- Frontend styling: `frontend/src/App.css`
- Audio settings: Both `main.py` and `App.jsx`

Happy coding! 🚀

