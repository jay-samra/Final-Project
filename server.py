# Abhijit Singh Ubhi, Jagmeet Singh, Jagroop Singh
# Dr. Syed Badruddoja
# Final Project

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
            data = data.decode().strip()
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
                    
            # command for user to quit the chat   
            elif data == "QUIT":
                if username in userDatabase:
                    # if user quits the chat, they must be deleted from 
                    # database to make space for new user
                    del userDatabase[username]
                    print(f"{username} is quitting hte server")
            
            # command to list all members of the voice chat
            elif data == "LIST":
                if username is not None:
                    # combining all members of the database using join
                    displayList = ", ".join(userDatabase.keys())
                    clientSocket.send(displayList.encode())
                    
            elif data.startswith("BCST "):
                if username is not None:
                    # message contains all the items of the string after the command
                    broadcastMsg = data[5:]
                    # sending the message to all members of the voicechat
                    clientSocket.send(f"{username} is sending a broadcast".encode())
                    # calling out Broadcast messaging function
                    bcstFunc(username, broadcastMsg)
            
                    
            elif data.startswith("MESG"):
                # spliting the user input since it contains MESG call and message string
                userInput = data.split()
                
                # storing the name of recepcient 
                recpName = userInput[1]
                # storing the message of the user
                message = " ".join(userInput[2:])
                
                # ensuring that user has enough arguments in command call
                if len(userInput) < 3:
                    print("Usage: MESG <User> <Message>")
                
                # is the recepient actually exists in the user database, only then can the message be sent
                if recpName in userDatabase:
                    try:
                        # sending message to apporiate user
                        userDatabase[recpName].send(f"{username}: {message} ".encode())
                    except:
                        clientSocket.send("Error".encode())
                
        
        
        except:
            break
    # connection closed
    clientSocket.close()
    
# function created for the broadcast function
def bcstFunc(username, message):
    # sending a message to all members of the chat except to self
    for name, userSocket in userDatabase.items():
        # ensuring msg is sent to everyone except the user
        if name != username:
            userSocket.send(f"{username}: {message}".encode())


def main():
    # COrrect usage shown in case of error
    if len(sys.argv) != 2:
        print("Usage: python3 server.py <server_port>")
        sys.exit(1)
    
    # storing the port number as an int
    port = int(sys.argv[1])

    # TCP server socket creation + binding
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # binding socket 
    serverSocket.bind(("0.0.0.0", port))
    
    serverSocket.listen(5)
    print("Socket is Listenting")
    
    
    # a forever loop until client wants to exit
    while True:
        
        # establish connection with client
        clientSocket, addr = serverSocket.accept()

        print('Connected to :', {addr})
        # Start a new thread by using threading func
        t1 = threading.Thread(target = threaded, args=(clientSocket,))
        
        t1.start()
    serverSocket.close()

if __name__ == "__main__":
    main()
