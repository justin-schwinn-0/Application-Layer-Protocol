import socket

HEADERSIZE = 10

def main():
    ###
    #serverIP = input("Server IP: ")
    #serverPort = int(input("Server Port: "))
    #renderIP = input("Renderer IP: ")
    #renderPort = int(input("Renderer Port: "))
    ###

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.connect((serverIP, serverPort))
    s.connect((socket.gethostname(), 1249)) # For testing on local host
    sendMsg(s, "client")

    r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ##r.connect((renderIP, renderPort))
    r.connect((socket.gethostname(), 1250)) # For testing on local host
    print("Commands: \"list\", \"render\", \"pause\", \"resume\", \"restart\", \"exit\"\n")

    userInput = ""
    message = ""
    while True:
        userInput = input("Input command: ")
        if userInput.lower() == "list":
            # Tells the server to send a list of media in a file
            ##sendMsg(s,"SendList")
            ##message = recieveMsg(s)
            continue
        elif userInput.lower() == "render":
            # Tells renderer to render a certain file
            userInput = input("Input file to render: ")
            sendMsg(r,userInput)
            message = recieveMsg(r)
            if message.lower() == "invalid":
                print("Invalid filename")
        elif userInput.lower() == "pause":
            # Send pause message to renderer
            sendMsg(r,"pause")
        elif userInput.lower() == "resume":
            # Send resume message to renderer
            sendMsg(r,"resume")
        elif userInput.lower() == "restart":
            # Send restart message to renderer
            sendMsg(r,"restart")
        elif userInput.lower() == "exit":
            break
        else:
            print("Invalid command\n")
    ##s.close()
    r.close()

def recieveMsg(sock):
    fullMsg = ""
    msgLen = 0
    newMsg = True
    while True:
        msg = sock.recv(20)
        if newMsg:
            msgLen = int(msg[:HEADERSIZE])
            newMsg = False

        fullMsg += msg.decode("utf-8")

        if len(fullMsg) - HEADERSIZE == msgLen:
            print("Full message is recieved")
            return fullMsg[HEADERSIZE:]

def sendMsg(sock, message):
    msg = f"{len(message):<{HEADERSIZE}}" + message
    sock.send(bytes(msg,"utf-8"))

if __name__ == "__main__":
    main()