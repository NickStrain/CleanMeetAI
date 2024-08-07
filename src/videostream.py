import cv2

def generate_frames():
    camera = cv2.VideoCapture(0)  
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

