import xml.etree.ElementTree as ET

def welcomeMessage():
    print("Welcome Message")

def memento():
    print("Memento")

def moveRequest():
    print("Move request")

def result():
    print("Result")

def parse_message(message):
    xml = ET.fromstring(message.decode())
    data = xml.find("data")
    
    match data.attrib["class"]:
        case "welcomeMessage":
            welcomeMessage()
        
        case "memento":
            memento()

        case "moveRequest":
            moveRequest()

        case "result":
            result()

        case _:
            print("Unknown data type:", data.attrib["class"])


