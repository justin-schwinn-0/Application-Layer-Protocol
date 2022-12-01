import socket

HEADERSIZE = 10
DEFAULT_SEG_SIZE = 256
COMMANDS = ["list","render","pause","resume","restart","exit"]

afnjk = "sendlist"
def main():
    ###
    #serverIP = input("Server IP: ")
    #serverPort = int(input("Server Port: "))
    ###

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ##s.connect((serverIP, serverPort))
    s.connect((socket.gethostname(), 31249))
    sendMsg(s, "renderer connected")

    r = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Binds the render to localhost port 1234
    ##r.bind((socket.gethostname(), 1235)) 
    r.bind((socket.gethostname(), 31250))
    r.listen(5)

    
    message = ""

    renderProgress = int()
    filename = ""

    clientSocket, clientAddress = r.accept()
    while True: # May need to use select to manage connections if issues arise
        message = recieveMsg(clientSocket)
        print(message)
        if message != False:
            if message == "render":
                print("Render received")

                filename = recieveMsg(clientSocket) # receive file name
                renderProgress = 0
                sendClientChunk(s,clientSocket,filename,renderProgress)

                # Ask the server to render a file, send invalid to client if no file found
            elif message == "pause":
                # Tell server to stop byte stream
                print("pause recieved")

            elif message == "resume": # Fix this
                # Tell server to send next packet
                print("resume recieved")

                ###
                #if(filename == ""):
                    #sendMsg(clientSocket,"Must choose a file to render first")
                #else:
                    #renderProgress+=DEFAULT_SEG_SIZE
                    #sendClientChunk(s,clientSocket,filename,renderProgress)
                ###

            elif message == "restart": # Fix this
                # Ask server to render message from the start
                print("restart recieved")
                
                ###
                #if(filename == ""):
                    #sendMsg(clientSocket,"Must choose a file to render first")
                #else:
                    #renderProgress = 0
                    #sendClientChunk(s,clientSocket,filename,renderProgress)
                ###

            ###
            #elif message == "list" : # unecessary delete once you fix the issue
                #print("list recieved")
                #sendMsg(s,message)
                #forwardMsg(s,clientSocket)
            ###

        else:
            print("Connection was forcibly closed")
            break

    # Find a way to break code once client disconnects from renderer
    s.close()

###
#def forwardMsg(sender:socket.socket, receiver:socket.socket): # Not necessary
    #d = sender.recv(DEFAULT_SEG_SIZE)
    #print(f"test {d}")
    #receiver.send(d) # No longer needed
    #return
###

def recieveMsg(sock:socket.socket)-> str:
    try:
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
                return fullMsg[HEADERSIZE:]
    except:
        return False

def sendMsg(sock:socket.socket, message:str):
    msg = f"{len(message):<{HEADERSIZE}}" + message
    sock.send(msg.encode())

def sendChunkRequest(s:socket.socket,filename:str,rProg:int):
    
    serverCommand = f"read {filename} {rProg}"

    print(f"sending: {serverCommand}")
    sendMsg(s, serverCommand)
    return

def sendClientChunk(s:socket.socket,c:socket.socket,filename:str,rProg:int):
    
    sendChunkRequest(s,filename=filename,rProg=rProg)
    d = s.recv(DEFAULT_SEG_SIZE)
    print(f"test {d}")
    ##forwardMsg(sender=s,receiver=c)


if __name__ == "__main__":
    main()