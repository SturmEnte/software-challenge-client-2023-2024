from network import Connection
from message_parser import parse_message

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 13050
LOG = True

connection = Connection(SERVER_HOST, SERVER_PORT, LOG)
connection.join()

print("Room Id:", connection.roomId)

game_info = {
    "team":None
}

while True:
    message = connection.receive_message()
    if message == 0:
        break
    elif message:
        print(message.decode())
        parsed = parse_message(message)

        if not parsed:
            continue

        match parsed[0]:
            case "t":
                if LOG:
                    print(f"Team: {parsed[1]}")
                game_info["team"] = parsed[1]

    
print("\n--- Finished execution of script ---")