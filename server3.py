import socket
import select
import sys  #for command line inputs
import json

BUFFER_SIZE = 8192 #buffer size

if __name__ == "__main__":
    #Command line input
    if len(sys.argv) < 2: #if the program was run with no port input in the command line, i.e "python server1.py"
        print("Usage: python server1.py <port number>") #print usage message 
        sys.exit(1) #return code 1 = error 
    port = int(sys.argv[1]) #argv[0] = script name; server1.py

    #Safe open dictioanry json file, and close after reading
    f = open("dictionary_compact.json", "r")
    dictionary = json.load(f)
    f.close()

    #1. Create server socket
    #Convert C to python: int my_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    socket_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

    #2. bind() on the IP+Port we want to listen on, use 0.0.0.0 to listen on all interfaces, client will use 127.0.0.1 for same-machine server/client
    socket_fd.bind(('0.0.0.0', port))   #.bind() takes a pair input: (host, port)

    #3. listen() on the IP+Port so that the socket can receive connection from a client
    socket_fd.listen(10) #The backlog parameter is 1, which means that concurrent clients will cause error, handled by OS 
    print("Server 1 listening on port: " + str(port) + "...")

    #Define a list of all client sockets that are currently connected to the server.
    clients = []
    #Define a list of all sockets including the server socket socket_fd to use for select()
    sockets = [socket_fd] 

    #Define infinite loop in a try block such that we can terminate the listening loop if there is a keyboardinterrupt
    try:
        #Create an infinite loop for server to listen for clients
        while True:
            """
            select.select checks the passed parameters (socket_list1, socket_list2, socket_list3, timeout_seconds) to see which sockets are
            readable in socket_list1, which sockets are writable in socket_list2, and which sockets have error in socket_list3. The return
            result is a list of 3 elements: readable, writable, and errored, each corresponding positionally to the list parameters. 
            Thus we check if socket_fd is currently ready for reading, and if it is, continue to accept() the connection. A socket being
            readable means that calling a socket function that requires input from the client won't wait indefinitely; implying that the client
            has a message queued for the socket. This prevents socket_fd.accept() from blocking any keyboard interrupts waiting for the client
            to connect to the server socket. The same concept applies to client_socket.recv(), as server.py will wait indefinitely and block
            ctrl+c until a message from the client is received. Thus apply select.select() to client_socket as well. 
            """
            readable, temp1, temp2 = select.select(sockets, [], [], 1.0)
            #Parse through the readable sockets, if the readable socket is socket_fd (server socket), then establish a new connection
            #if there is no client connected, or reject the new client since this is a single server and only allows 1 client at a time.
            for socket in readable:
                #If the server sockeet socket_fd is readable, a new connection is ready to accept
                if socket == socket_fd:
                    #4. accept() a client given socket_fd by calling accept() so that a connection between server and client is 
                    #established in python, socket.accept() returns 2 values, socket for data retrieval and client addr
                    client_socket, client_addr = socket_fd.accept()
                    client_socket.send("Connection established.".encode())
                    print("Server 1 connected with:", client_addr)
                    clients.append(client_socket)
                    sockets.append(client_socket)
                #if the current socket is readable and it is a client socket already connected, handle communication
                elif socket in clients:
                    #5. Receive data from client socket
                    data_raw = socket.recv(BUFFER_SIZE) #recv() returns bytes, to convert to a string, use .decode()
                    if not data_raw: #if data is NULL, client terminated via ctrl+c
                        print("Client", socket.getpeername(), "closed conection.")
                        clients.remove(socket)  #remove from list
                        sockets.remove(socket)  #remove from list
                        socket.close() #Close connection
                        continue
                    data = data_raw.decode()
                    print("Server 1 received data from client:", data)

                    response = dictionary.get(data) #Generate response for client's word
                    if response:
                        print("Definition found.")
                        socket.send((response + "\n").encode()) #Send response to client, needs bytes therefore convert via .encode()
                    else:
                        print("Definition not found.")
                        socket.send("Definition not found.".encode()) 
    except KeyboardInterrupt:   #If ctrl+c, break loop and stop listening for clients
        print("Server 1 severing connection(forcibly closed: ctrl+c).")

    print("Server1 Finished.")
    socket_fd.close()