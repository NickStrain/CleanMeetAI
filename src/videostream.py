import cv2


def cam():
    # Open a video capture
    cap = cv2.VideoCapture('udp://127.0.0.1:80',cv2.CAP_FFMPEG)  # 0 for default camera


    while True:
        ret, frame = cap.read()

       
        if not ret:
            break


if __name__ == '__main__':
    cam()