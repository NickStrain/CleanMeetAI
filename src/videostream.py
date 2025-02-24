import cv2 
import numpy as np
import torch 
import pyvirtualcam 
from PIL import Image 
from model_pipline import nsfwModel
import threading 

nsfw_model = nsfwModel()

def detect_nsfw(frame):
    # frame =  Image.fromarray(frame)
    out = nsfw_model.predict(frame)
    return out 

def overlay_prediction(frame, label):
    """ Overlay NSFW detection result on the frame """
    if label == "nsfw":
        color = (0, 0, 255)  # Red warning text
        text = "Offensive Video Detected!"
        cv2.rectangle(frame, (0, 0), (frame.shape[1], 100), (0, 0, 255), -1)  # Red box at top
    else:
        color = (0, 255, 0)  # Green safe text
        text = "Video is Safe"
        cv2.rectangle(frame, (0, 0), (frame.shape[1], 100), (0, 255, 0), -1)  # Green box at top
    cv2.putText(frame, text, (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
    return frame

cap = cv2.VideoCapture(0) 

with pyvirtualcam.Camera(width=640, height=480, fps=60, print_fps=True) as cam:
    print("Virtual Camera started...",flush = True)

    while True:
        ret, frame = cap.read()
        frame_rgb_out = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
      
        label = detect_nsfw(frame_rgb_out)
        frame = overlay_prediction(frame_rgb_out, label)
        cam.send(frame)
        print(label,flush=True)
        
        


cap.release()
cv2.destroyAllWindows()
# import colorsys
# import numpy as np
# import pyvirtualcam

# with pyvirtualcam.Camera(width=1920, height=1080, fps=30, print_fps=True) as cam:
#     print(f'Using virtual camera: {cam.device}')
#     frame = np.zeros((cam.height, cam.width, 3), np.uint8)  # RGB
#     while True:
#         h, s, v = (cam.frames_sent % 100) / 100, 1.0, 1.0
#         r, g, b = colorsys.hsv_to_rgb(h, s, v)
#         frame[:] = (r * 255, g * 255, b * 255)
#         cam.send(frame)
#         cam.sleep_until_next_frame()