import cv2
import asyncio
from PIL import Image
from model_pipline import nsfwModel
import time
import sys

def generate_frames():
    camera =cv2.VideoCapture(0) 
    while True:
        success, frame = camera.read()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame =  Image.fromarray(frame)
        yield (frame)
            

def pre():
    model = nsfwModel()
    camera = cv2.VideoCapture(0)
    while True:
        success,frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame =  Image.fromarray(frame)
        out = model.predict(frame)
        yield out

for i in pre():
    print(i)
    sys.stdout.flush()
  