# Abhijit Singh Ubhi, Jagmeet Singh, Jagroop Singh
# Dr. Syed Badruddoja
# Final Project

import sys
import socket
import threading


def main():
    # ensuring that the user has enough arguments in their client call
    if len(sys.argv) != 3:
        print("Usage: python3 server.py <server_ip> <server_port>")
        sys.exit(1)
        
    # socket object is passed as a argument 
    def reciever(socket):
        # function always recieved data from socket
        while True:
            try:
                # recieving data from the socket
                data = socket.recv(1024)
                if not data:
                    break
                # displaying the data from the socket
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
    
    # using threaing function to create threads which allow user to carry  out multiple actions
    threading.Thread(target=reciever, args=(clientSocket,)).start()
    
    # User must user JOIN to enter chat
    print("Please enter JOIN followed by name: ")
    newUser = input()
    
    # sending the name of the new user
    clientSocket.send(newUser.encode())
    
    
    
    while True:
        userCommand = input()
        clientSocket.send(userCommand.encode())
        # exiting program 
        if userCommand == "QUIT":
            break
        
    # always closing the socket
    clientSocket.close()
    
if __name__ == "__main__":
    main()
    
    
    
        
