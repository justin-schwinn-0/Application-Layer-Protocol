import socket

HEADERSIZE = 10

def main():
    serverIP = input("Server IP: ")
    serverPort = input("Server Port: ")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((serverIP, serverPort))
    sendMsg(s, "renderer")

    r = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Binds the render to localhost port 1234
    r.bind((socket.gethostname(), 1234)) 
    r.listen(5)

    while True:
        break # checks to see if anything connected with renderer

    s.close()

def recieveMsg(sock):
    fullMsg = ""
    msgLen = 0
    newMsg = True
    while True:
        msg = s.recv(20)
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