# import socket
# import requests

# # UDP setup
# udp_ip = "127.0.0.1"
# udp_port = 80

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind((udp_ip, udp_port))

# # HTTP setup
# http_url = "http://127.0.0.1:80"

# while True:
#     data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
#     print(f"Received message: {data} from {addr}")
    
#     # Translate UDP data to HTTP POST request
#     response = requests.post(http_url, data=data)
#     print(f"HTTP response status code: {response.status_code}")
#     print(f"HTTP response content: {response.text}")
