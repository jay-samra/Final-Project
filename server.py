
import sys
import socket
import threading

userDatabase = dict()

# thread function
def threaded(clientSocket):
    username = None
    while True:
        try:
            # data received from client
            data = clientSocket.recv(1024)
            if not data:
                print('Disconnecting')
                break
            
            # using startwith() to check if user inputed JOIN
            if data.startswith("JOIN "):
                
                # storing the user inputted name
                name = data.split()[1]
                if len(userDatabase) > 10:
                    # Reject new user if current users are over 10
                    clientSocket.send("Too Many Users".encode())
                # store new user in database if there is space in the chat
                elif len(userDatabase) <= 10:
                    userDatabase[name] = clientSocket
                    username = name
                    print(f"{username} has joined the chat")
                    
                
            elif data == "QUIT":
                if username is not None:
                    userDatabase(data).pop()
                    print(f"{username} is quitting hte server")
                    
            elif data == "LIST":
                if username is not None:
                    displayList = ", ".join(userDatabase.keys())
                    clientSocket.send(displayList.encode())
                    
            elif data.startswith("BCST "):
                if username is not None:
                    # message contains all the items of the string after the command
                    broadcastMsg = data[5:]
                    clientSocket.send(f"{username} is sending a broadcast".encode())
                    
                
        
        
        except:
            break
    # connection closed
    clientSocket.close()


def main():
    # COrrect usage shown in case of error
    if len(sys.argv) != 2:
        print("Usage: python3 server.py <server_port>")
        sys.exit(1)
        
    port = int(sys.argv[1])

    # TCP server socket creation + binding
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(("0.0.0.0", port))
    
    serverSocket.listen(5)
    print("Socket is Listenting")
    
    
    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        clientSocket, addr = serverSocket.accept()
        # lock acquired by client
        # print_lock.acquire()
        print('Connected to :', {addr})
        # Start a new thread and return its identifier
        t1 = threading.Thread(target = threaded, args=(clientSocket,))
        # receive_thread = threading.Thread(target=receive,args=(nickname, client_socket,))
        t1.start()
    serverSocket.close()

if __name__ == "__main__":
    main()
