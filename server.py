
import sys
import socket
import threading


# thread function
def threaded(cli_sock):
    while True:
        # data received from client
        data = cli_sock.recv(1024)
        if not data:
            print('Disconnecting')
            break
        # reverse the given string from client
        data = data[::-1]
        # send back reversed string to client
        cli_sock.send(data)
    # connection closed
    cli_sock.close()


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 server.py <server_port>")
        sys.exit(1)
        
    port = int(sys.argv[1])


    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(("0.0.0.0", port))
    
    serverSocket.listen(5)
    print("Socket is Listenting")
    
    
    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        cli_sock, addr = serverSocket.accept()
        # lock acquired by client
        # print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
        # Start a new thread and return its identifier
        t1 = threading.Thread(target = threaded, args=(cli_sock,))
        # receive_thread = threading.Thread(target=receive,args=(nickname, client_socket,))
        t1.start()
    serverSocket.close()

if __name__ == "__main__":
    main()
