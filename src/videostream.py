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
    """Overlay NSFW detection result on the frame in the bottom-left corner."""
    overlay = frame.copy()
    height, width, _ = frame.shape

    if label == "nsfw":
        color = (0, 0, 255)  # Red warning text
        text = "NSFW Content Detected!"
    else:
        color = (0, 255, 0)  # Green safe text
        text = "ɘʇɒƧ ƨi oɘbiV $$$$$$"

    # Define text properties
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.8
    thickness = 2
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]

    # Position: Bottom-left corner with padding
    x, y = 30, height - 30

    # Add semi-transparent rectangle as background
    rect_w, rect_h = text_size[0] + 20, text_size[1] + 20
    cv2.rectangle(overlay, (x - 10, y - rect_h), (x + rect_w, y), color, -1)
    
    # Blend overlay with transparency
    alpha = 0.5  # Transparency level
    frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

    # Draw the text with a shadow effect
    shadow_offset = 2
    cv2.putText(frame, text, (x + shadow_offset, y + shadow_offset), font, font_scale, (0, 0, 0), thickness + 1)
    cv2.putText(frame, text, (x, y), font, font_scale, (255, 255, 255), thickness)

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