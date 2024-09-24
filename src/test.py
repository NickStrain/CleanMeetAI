from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
speech_to_text = pipeline("automatic-speech-recognition", model="facebook/wav2vec2-large-960h")

@app.websocket("/wsaudio")
async def websocket_audio(websocket: WebSocket):
    await websocket.accept()

    try:
        audio_data = await websocket.receive_bytes()
        transcript = speech_to_text(audio_data)["text"]
        print(transcript,flush=True)

        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        await websocket.close()
