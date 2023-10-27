import xml.etree.ElementTree as ET

def welcomeMessage(data):
    print("Welcome Message")
    return ("t",data.attrib["color"])
    

def memento(data):
    print("Memento")

def moveRequest(data):
    print("Move request")

def result(data):
    print("Result")

def parse_message(message):
    xml = ET.fromstring(message.decode())
    data = xml.find("data")
    
    match data.attrib["class"]:
        case "welcomeMessage":
            return welcomeMessage(data)
        
        case "memento":
            return memento(data)

        case "moveRequest":
            return moveRequest(data)

        case "result":
            return result(data)

        case _:
            print("Unknown data type:", data.attrib["class"])


