# CleanMeetAI

https://github.com/i99dev/Docker-with-WebCam/tree/master?tab=readme-ov-file

ffmpeg -list_devices true -f dshow -i dummy
ffmpeg -f dshow -framerate 30 -i video="Integrated Camera" -vcodec mpeg4 -q 12 -f mpegts udp://127.0.0.1:80

ffmpeg -i udp://127.0.0.1:80 -c copy -f mpegts http://127.0.0.1:80
