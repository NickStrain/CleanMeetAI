import cv2
from fastapi import FastAPI, Request,BackgroundTasks,WebSocket,WebSocketDisconnect,UploadFile,File
import numpy as np
import asyncio
from PIL import Image
from fastapi.responses import StreamingResponse
# from sse_starlette.sse import EventSourceResponse
import json
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import sys
import io
import soundfile as sf
# from videostream import generate_frames
from model_pipline import nsfwModel,ConnectionManager
from transformers import pipeline
import time
app = FastAPI()
buffer_manager =  ConnectionManager()
origins = [

    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:80",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

def generate_cam_frame():
    camera =cv2.VideoCapture(0) 
    if not camera.isOpened():
        raise RuntimeError("Could not start camera.")
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
def video_pre(model):
    model = model
    camera = cv2.VideoCapture(0)
    while True:
        success,frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame =  Image.fromarray(frame)
        out = model.predict(frame)
        json_output = json.dumps({"prediction": out})
        sys.stdout.flush()
        yield f"{json_output}\n"
        time.sleep(1) 

        
    

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


# for i in pre():
#     print("sdf",i)
#     time.sleep(2)



# camera =cv2.VideoCapture('udp://127.0.0.1:80', cv2.CAP_FFMPEG) 

# while True:
#     success,frame = camera.read()
#     print(frame)


