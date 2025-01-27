import cv2
import threading
from fastapi import FastAPI, Request,BackgroundTasks,WebSocket,WebSocketDisconnect,UploadFile,File
import numpy as np
import asyncio
from PIL import Image
from fastapi.responses import StreamingResponse
import json
from model_pipline import Textclassifier
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import sys
import io
from io import BytesIO
import soundfile as sf
# from videostream import generate_frames
from model_pipline import nsfwModel,ConnectionManager
from transformers import pipeline
import time
from pydub import AudioSegment

app = FastAPI()
buffer_manager =  ConnectionManager()
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (replace with specific origins for more security)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

nsfw_model = nsfwModel()
pipe = pipeline("automatic-speech-recognition", model="openai/whisper-small.en")
text_cl_model= Textclassifier()

def detect_nsfw_video(image: Image.Image) -> dict:
    image = image.convert("RGB")
    predictions = nsfw_model.predict(image)
    return predictions

def process_audio(file: BytesIO):
    audio = AudioSegment.from_file(file, format="wav")  # Load the audio file using pydub
    audio = audio.set_channels(1)  # Set to mono
    audio = audio.set_frame_rate(16000)

    # Load the audio file using soundfile (can handle various formats)
    wav_io = io.BytesIO()
    audio.export(wav_io, format="wav")
    wav_io.seek(0)  # Reset buffer position for reading

    # Now, try reading with soundfile
    
    data, samplerate = sf.read(wav_io)
    # Use Whisper to transcribe the audio into text
    transcription = pipe(audio_data)["text"]
    return transcription

@app.post("/detect-nsfw")
async def detect_nsfw_endpoint(file: UploadFile):
    image_data = await file.read()
    image = Image.open(BytesIO(image_data))
    predictions = detect_nsfw_video(image) 
    # print(predictions,flush = True)
    return predictions

@app.post("/detect-audio")
async def detect_audio_endpoint(file: UploadFile):
    audio_data = await file.read()
    
    # Process the audio (transcribe and classify)
    transcription = process_audio(BytesIO(audio_data))
    print(transcription,flush= True)
    pred = text_cl_model.pred(transcript) 
    return pred


@app.get("/")
def index(request:Request):
    context = {"request":request}
    return templates.TemplateResponse("index.html",context=context)

@app.get("/video")
def video():
    return StreamingResponse(generate_cam_frame(), media_type='multipart/x-mixed-replace; boundary=frame')

@app.get("/output")
async def video_pre_endpoint():
    return StreamingResponse(video_pre(nsfwModel()), media_type="text/event-stream")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    for i in video_pre(nsfwModel()):
        out = json.dumps({"pre":i})
        await websocket.send_text(out)
        await asyncio.sleep(1)

speech2text_model = pipeline("automatic-speech-recognition", model="facebook/wav2vec2-large-960h")



@app.websocket("/wsaudio")
async def websocket_audio(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            # Receive audio data from client
            audio_data = await websocket.receive_bytes()

            # Process audio with Whisper (speech-to-text)
            transcript = pipe(audio_data)

            # Run text classification for offensive content detection
            pred = text_cl_model.pred(transcript["text"])
            print(pred[0]['label'],flush=True)

            await websocket.send_text(pred[0]['label'],)
            # Send response back to client if needed (for real-time updates)
            # (Optional: return offensive/NSFW detection result to the frontend)
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        await websocket.close()