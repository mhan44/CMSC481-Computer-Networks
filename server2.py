from multiprocessing import Process
import socket
import select
import sys  #for command line inputs
import json

BUFFER_SIZE = 8192 #buffer size

#Safe open dictioanry json file, and close after reading
f = open("dictionary_compact.json", "r")
dictionary = json.load(f)
f.close()

#Define a function that handles client communication, because Process() needs a target
def connect(current_socket, current_addr):
    while True:
        #5. Receive data from client socket
        data_raw = current_socket.recv(BUFFER_SIZE) #recv() returns bytes, to convert to a string, use .decode()
        if not data_raw: #if data is NULL, client terminated via ctrl+c
            print("Client", current_addr, "closed conection.")    
            current_socket.close() #Close connection
            break
        data = data_raw.decode()
        print("Server 1 received data from client " + str(current_addr) + ": ", data)

        response = dictionary.get(data) #Generate response for client's word
        if response:
            print("Definition found.")
            current_socket.send((response + "\n").encode()) #Send response to client, needs bytes therefore convert via .encode()
        else:
            print("Definition not found.")
            current_socket.send("Definition not found.".encode()) 


if __name__ == "__main__":
    #Command line input
    if len(sys.argv) < 2: #if the program was run with no port input in the command line, i.e "python server1.py"
        print("Usage: python server1.py <port number>") #print usage message 
        sys.exit(1) #return code 1 = error 
    port = int(sys.argv[1]) #argv[0] = script name; server1.py

    #1. Create server socket
    #Convert C to python: int my_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    socket_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

    #2. bind() on the IP+Port we want to listen on, use 0.0.0.0 to listen on all interfaces, client will use 127.0.0.1 for same-machine server/client
    socket_fd.bind(('0.0.0.0', port))   #.bind() takes a pair input: (host, port)

    #3. listen() on the IP+Port so that the socket can receive connection from a client
    socket_fd.listen(10) #The backlog parameter is 10, which means that concurrent clients are allowed
    print("Server 1 listening on port: " + str(port) + "...")

    #Define infinite loop in a try block such that we can terminate the listening loop if there is a keyboardinterrupt
    try:
        #Create an infinite loop for server to listen for clients
        while True:
            readable, temp1, temp2 = select.select([socket_fd], [], [], 1.0)
            if socket_fd in readable:
                #4. accept() a client given socket_fd by calling accept() so that a connection between server and client is 
                #established in python, socket.accept() returns 2 values, socket for data retrieval and client addr
                current_socket, current_addr = socket_fd.accept()
                current_socket.send("Connection established.".encode())
                print("Server 1 connected with:", current_addr)

                #Fork(create new process using multiprocess) to handle new clients
                newClient = Process(target=connect, args=(current_socket, current_addr))
                newClient.start()
            
    except KeyboardInterrupt:   #If ctrl+c, break loop and stop listening for clients
        print("Server 1 severing connection(forcibly closed: ctrl+c).")

    print("Server1 Finished.")
    socket_fd.close() 