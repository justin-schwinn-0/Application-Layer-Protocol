import socket
import select
import sys

serverIP = "gfhjbmjkhgkvb"
renderIP = ""

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
    s.connect((serverIP, 31249))
    sendMsg(s, "renderer connected")

    r = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Binds the render to localhost port 1234
    ##r.bind((socket.gethostname(), 1235)) 
    r.bind((renderIP, 32250))
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
                renderFile3(s,clientSocket,filename,renderProgress)

                # Ask the server to render a file, send invalid to client if no file found
            elif message == "pause":
                # Tell server to stop byte stream
                print("pause inactive, start rendering to use command")

            elif message == "resume": # Fix this
                # Tell server to send next packet
                print("resume inactive, start rendering to use command")

                ###
                #if(filename == ""):
                    #sendMsg(clientSocket,"Must choose a file to render first")
                #else:
                    #renderProgress+=DEFAULT_SEG_SIZE
                    #sendClientChunk(s,clientSocket,filename,renderProgress)
                ###

            elif message == "restart": # Fix this
                # Ask server to render message from the start
                print("restart inactive, start rendering to use command")
                
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
"""
def recieveMsg(sock:socket.socket)-> str:
    try:
        fullMsg = ""
        msgLen = 0
        newMsg = True
        while True:
            msg = sock.recv(DEFAULT_SEG_SIZE + 10)
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
    print(f"sent: {msg}")
"""

def recieveMsg(sock:socket.socket)-> str:
    return sock.recv(DEFAULT_SEG_SIZE)

def sendMsg(sock:socket.socket, message):
    sock.send(message.encode())


def sendChunkRequest(s:socket.socket,filename:str,rProg:int):
    
    serverCommand = f"read {filename} {rProg}"
    #print(f"Sending Server command: {serverCommand}")
    sendMsg(s, serverCommand)

def renderFile3(s:socket.socket, c:socket.socket, filename:str,rProgress:int):
    sendChunkRequest(s,filename=filename,rProg=rProgress)
    fs = int(recieveMsg(s))
    print(fs)
    d = recieveMsg(s)
    print(d)


def renderFile(s:socket.socket, c:socket.socket, filename:str,rProg:int): # This function is redundant remove and fix once everything is working
    if rProg == 0:
        sendChunkRequest(s,filename=filename,rProg=rProg)
        fileSize = recieveMsg(s)
        print(fileSize)
        #d = s.recv(DEFAULT_SEG_SIZE)
        d = recieveMsg(s)
        print(d)
        rProg += DEFAULT_SEG_SIZE



    c.setblocking(0) # Added to get the pause, resume, restart working
    paused = False

    while fileSize > rProg:
        ready = select.select([c], [], [], 0.25) # Added
        if ready[0]:
            data = recieveMsg(c)
            if data == "pause":
                print("pausing stream")
                paused = True

            elif data == "resume": # Fix this
                print("resuming stream")
                paused = False

            elif data == "restart":
                print("restarting stream")
                rProg = -1
            elif data == "exit": # kinda iffy. May break code
                print("exiting")
                break
            else:
                print("command not recognized")
        elif paused == False: 
            #time.sleep(0.5)
            #print(f"looping filesize: {fileSize}, proggress: {rProg}")
            sendChunkRequest(s,filename=filename,rProg=rProg)
            if rProg == -1:
                rProg = 0
            #d = s.recv(DEFAULT_SEG_SIZE)
            d = recieveMsg(s)
            print(f"test {d}")
            rProg += DEFAULT_SEG_SIZE
            ##forwardMsg(sender=s,receiver=c)
    c.setblocking(1)

def renderFile2(s:socket.socket, c:socket.socket, filename:str,rProg:int): # This function is redundant remove and fix once everything is working
    if rProg == 0:
        print("progress is 0")
        sendChunkRequest(s,filename=filename,rProg=rProg)
        fileSize = int(recieveMsg(s))
        print(f"Filesize: {fileSize}")
        #d = s.recv(DEFAULT_SEG_SIZE)
        d = recieveMsg(s)
        print(f"test {d}")
        rProg += DEFAULT_SEG_SIZE

    c.setblocking(0) # Added to get the pause, resume, restart working
    paused = False

    while fileSize > rProg:
        ready = select.select([c], [], [], 0.25) # Added
        if ready[0]:
            data = recieveMsg(c)
            if data == "pause":
                print("pausing stream")
                paused = True

            elif data == "resume": # Fix this
                print("resuming stream")
                paused = False

            elif data == "restart":
                print("restarting stream")
                rProg = -1
            elif data == "exit": # kinda iffy. May break code
                print("exiting")
                break
            else:
                print("command not recognized")
        elif paused == False: 
            #time.sleep(0.5)
            #print(f"looping filesize: {fileSize}, proggress: {rProg}")
            sendChunkRequest(s,filename=filename,rProg=rProg)
            if rProg == -1:
                rProg = 0
            #d = s.recv(DEFAULT_SEG_SIZE)
            d = recieveMsg(s)
            print(f"test {d}")
            rProg += DEFAULT_SEG_SIZE
            ##forwardMsg(sender=s,receiver=c)
    c.setblocking(1)


if __name__ == "__main__":
    if(len(sys.argv) != 3):
        print("Invalid arguments, try Rednerer.py <server IP> <Renderer IP>")
        exit()
    else:
        serverIP = sys.argv[1]
        renderIP = sys.argv[2]
    main()