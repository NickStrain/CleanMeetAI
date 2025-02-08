import cv2
import numpy as np
import torch
import pyvirtualcam
import threading
from queue import Queue
from model_pipline import nsfwModel

nsfw_model = nsfwModel()

def detect_nsfw(frame, result_queue):
    """Runs NSFW detection asynchronously"""
    with torch.no_grad():  # Disable gradient computation for faster inference
        label = nsfw_model.predict(frame)
    result_queue.put(label)

def overlay_prediction(frame, label):
    """Overlay NSFW detection result on the frame"""
    if label == "nsfw":
        color = (0, 0, 255)  # Red warning text
        text = "Offensive Video Detected!"
        cv2.rectangle(frame, (0, 0), (frame.shape[1], 100), (0, 0, 255), -1)
    else:
        color = (0, 255, 0)  # Green safe text
        text = "Video is Safe"
        cv2.rectangle(frame, (0, 0), (frame.shape[1], 100), (0, 255, 0), -1)
    
    cv2.putText(frame, text, (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
    return frame

# Capture from webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 30)  # Ensure high FPS
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Queue to hold the latest NSFW detection result
result_queue = Queue()
latest_label = "safe"  # Default label

with pyvirtualcam.Camera(width=640, height=480, fps=30, print_fps=True) as cam:
    print("Virtual Camera started...", flush=True)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb_out = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Start NSFW detection in a separate thread without blocking
        if not threading.active_count() > 2:  # Prevent thread overflow
            threading.Thread(target=detect_nsfw, args=(frame_rgb_out, result_queue), daemon=True).start()
        
        # Get latest NSFW detection result if available
        if not result_queue.empty():
            latest_label = result_queue.get()

        # Overlay label and send frame to virtual cam
        frame_with_overlay = overlay_prediction(frame_rgb_out, latest_label)
        cam.send(frame_with_overlay)

        print(latest_label, flush=True)

cap.release()
cv2.destroyAllWindows()
