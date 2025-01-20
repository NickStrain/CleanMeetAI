from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import torch 
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
device = "cuda:0" if torch.cuda.is_available() else "cpu"

pipe = pipeline("automatic-speech-recognition", model="openai/whisper-base.en")

@app.websocket("/wsaudio")
async def websocket_audio(websocket: WebSocket):
    await websocket.accept()

    try:
        audio_data = await websocket.receive_bytes()
        # transcript = speech_to_text(audio_data)["text"]
        transcript = pipe(audio_data)
        print(transcript,flush=True)
       
        

        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        await websocket.close()