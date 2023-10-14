import xml.etree.ElementTree as ET

from network import Connection
from message_parser import parse_message

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 13050
LOG = True

connection = Connection(SERVER_HOST, SERVER_PORT, LOG)
connection.join()

print("Room Id:", connection.roomId)

while True:
    message = connection.receive_message()
    if message == 0:
        break
    elif message:
        print(message.decode())
        parse_message(message)
    
print("\n--- Finished execution of script ---")