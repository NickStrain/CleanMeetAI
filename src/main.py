import cv2
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
# from videostream import generate_frames
app = FastAPI()
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

def generate_frames():
    camera =cv2.VideoCapture('udp://127.0.0.1:80', cv2.CAP_FFMPEG) 
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


@app.api_route("/", methods=["GET", "POST"])
def index(request:Request):
    context = {"request":request}
    return templates.TemplateResponse("index.html",context=context)

@app.api_route("/video", methods=["GET", "POST"])
def video():
    return StreamingResponse(generate_frames(), media_type='multipart/x-mixed-replace; boundary=frame')

# camera =cv2.VideoCapture('udp://127.0.0.1:80', cv2.CAP_FFMPEG) 

# while True:
#     success,frame = camera.read()
#     print(frame)


