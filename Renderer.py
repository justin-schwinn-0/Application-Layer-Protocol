import socket

HEADERSIZE = 10

def main():
    serverIP = input("Server IP: ")
    serverPort = input("Server Port: ")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((serverIP, serverPort))
    sendMsg(s, "renderer")

    r = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Binds the render to localhost port 1234
    r.bind((socket.gethostname(), 1235)) 
    r.listen(5)

    rendering = False
    message = ""

    while True: # May need to use select to manage connections if issues arise
        clientSocket, clientAddress = r.accept()
        message = recieveMsg(clientSocket)
        if message.lower() == "render":
            message = recieveMsg(r)
            # Ask the server to render a file, send invalid to client if no file found
        elif message.lower() == "pause":
            # Tell server to stop byte stream
            sendMsg(r,"pause")
        elif message.lower() == "resume":
            # Tell server to resume byte stream
            sendMsg(r,"resume")
        elif message.lower() == "restart":
            # Ask server to render message from the start
            sendMsg(r,"restart")

    # Find a way to break code once client disconnects from renderer
    s.close()

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
            return fullMsg

def sendMsg(sock, message):
    msg = f"{len(message):<{HEADERSIZE}}" + message
    sock.send(bytes(msg,"utf-8"))

if __name__ == "__main__":
    main()