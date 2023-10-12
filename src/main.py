import socket
import xml.etree.ElementTree as ET


ET.fromstring('<joined roomId="7d45f6a2-7405-4915-862d-b50768b1172d"/>')

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 13050

# Setup connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_HOST, SERVER_PORT))

# Join game
request_xml = "<protocol>"
sock.sendall(request_xml.encode('utf-8'))

request_xml = "<join />"
sock.sendall(request_xml.encode('utf-8'))

# Game data
room_id = ""

while True:
    data = sock.recv(1024).decode('utf-8')
    
    if data and "joined" in data:
        data = data.split("\n")[1]
        raw = ET.fromstring(data)
        room_id = raw.attrib["roomId"]
        print(f"Room ID: {room_id}")
