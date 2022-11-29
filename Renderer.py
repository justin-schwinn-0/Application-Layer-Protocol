import socket

HEADERSIZE = 10

def main():
    ###
    #serverIP = input("Server IP: ")
    #serverPort = int(input("Server Port: "))
    ###

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ##s.connect((serverIP, serverPort))
    s.connect((socket.gethostname(), 1249))
    sendMsg(s, "renderer")

    r = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Binds the render to localhost port 1234
    ##r.bind((socket.gethostname(), 1235)) 
    r.bind((socket.gethostname(), 1250))
    r.listen(5)

    rendering = False
    message = ""

    while True: # May need to use select to manage connections if issues arise
        clientSocket, clientAddress = r.accept()
        message = recieveMsg(clientSocket)
        print(message)
        if message.lower() == "render":
            message = recieveMsg(r)
            print("render recieved!!!")
            # Ask the server to render a file, send invalid to client if no file found
        elif message.lower() == "pause":
            # Tell server to stop byte stream
            print("pause recieved!!!")
            ##sendMsg(s,"pause")
        elif message.lower() == "resume":
            # Tell server to resume byte stream
            print("resume recieved!!!")
            ##sendMsg(s,"resume")
        elif message.lower() == "restart":
            # Ask server to render message from the start
            print("restart recieved!!!")
            ##sendMsg(s,"restart")

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
            return fullMsg[HEADERSIZE:]

def sendMsg(sock, message):
    msg = f"{len(message):<{HEADERSIZE}}" + message
    sock.send(bytes(msg,"utf-8"))

if __name__ == "__main__":
    main()