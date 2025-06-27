import sys
import socket
import threading


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 server.py <server_ip> <server_port>")
        sys.exit(1)
        
    def reciever(socket):
        while True:
            try:
                data = socket.recv(1024)
                if not data:
                    break
                print("Recieved from server: ", str(data.decode()))
            except:
                break
        
    # storing the input 
    host = sys.argv[1]
    port = int(sys.argv[2])
    
    # creating socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # connecting to the server
    clientSocket.connect((host ,port))
    
    threading.Thread(target=reciever, args=(clientSocket,)).start()
    
    # User must user JOIN to enter chat
    print("Please enter JOIN followed by name: ")
    newUser = input()
    
    clientSocket.send(newUser.encode())
    
    
    
    while True:
        userCommand = input()
        clientSocket.send(userCommand.encode())
        if userCommand == "QUIT":
            break
        
    clientSocket.close()
    
if __name__ == "__main__":
    main()
    
    
    
        
