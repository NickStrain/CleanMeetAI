import cv2
import threading
from fastapi import FastAPI, Request,BackgroundTasks,WebSocket,WebSocketDisconnect,UploadFile,File
import numpy as np
import asyncio
from PIL import Image
from fastapi.responses import StreamingResponse
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

class CameraManager:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            raise RuntimeError("Could not open camera.")
        self.lock = threading.Lock()
        self.latest_frame = None
        self.running = True
        self.thread = threading.Thread(target=self._capture_frames, daemon=True)
        self.thread.start()

    def _capture_frames(self):
        while self.running:
            success, frame = self.camera.read()
            if success:
                with self.lock:
                    self.latest_frame = frame

    def get_frame(self):
        with self.lock:
            return self.latest_frame

    def stop(self):
        self.running = False
        self.thread.join()
        self.camera.release()

# Create a shared camera manager instance
camera_manager = CameraManager()

def generate_cam_frame():
   
    while True:
        frame = camera_manager.get_frame()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
def video_pre(model):
    model = model
    while True:
        frame = camera_manager.get_frame()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame =  Image.fromarray(frame)
        out = model.predict(frame)
        json_output = json.dumps({"prediction": out})
        sys.stdout.flush()
        yield f"{json_output}\n"
        # time.sleep(1) 


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


