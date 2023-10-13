import xml.etree.ElementTree as ET

from network import Connection

# ET.fromstring('<joined roomId="7d45f6a2-7405-4915-862d-b50768b1172d"/>')

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 13050

# Setup connection
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect((SERVER_HOST, SERVER_PORT))

# Join game
# request_xml = "<protocol>"
# sock.sendall(request_xml.encode('utf-8'))

# request_xml = "<join />"
# sock.sendall(request_xml.encode('utf-8'))

# Game data
# room_id = ""

# buffer = ""

connection = Connection(SERVER_HOST, SERVER_PORT, True)
connection.join()

# while True:
    # messages = connection.receive_messages()
    
    # buffer += sock.recv(1024).decode('utf-8')

    # print("Buffer")
    # print(buffer)
    # print("----")

    
    # if "joined" in buffer:
    #     data = buffer.split("\n")[1]
    #     raw = ET.fromstring(data)
    #     room_id = raw.attrib["roomId"]
    #     print(f"Room ID: {room_id}")
    #     buffer = ""
    # elif "<room" in buffer and "</room>" in buffer:
    #     raw = ET.fromstring(buffer)
    #     data = raw.find("data")
    #     print(data.attrib)
    #     buffer = ""

print("Room Id:", connection.roomId)

while True:
    messages = connection.receive_messages()
    if messages:
        print(messages.decode())
    