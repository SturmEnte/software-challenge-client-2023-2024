import xml.etree.ElementTree as ET

from network import Connection

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 13050
LOG = True

connection = Connection(SERVER_HOST, SERVER_PORT, LOG)
connection.join()

print("Room Id:", connection.roomId)

while True:
    messages = connection.receive_messages()
    if messages == 0:
        break
    elif messages:
        print(messages.decode())
    
print("\n--- Finished execution of script ---")