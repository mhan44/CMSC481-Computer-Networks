import socket
import select
import os
import sys  #for command line inputs

BUFFER_SIZE = 8192

if __name__ == "__main__":
    #Command line input
    if len(sys.argv) < 3: #if the program was run with no port input in the command line, i.e "python server1.py"
        print("Usage: python server1.py <IP> <port number>") #print usage message 
        sys.exit(1) #return code 1 = error 
        
    addr = sys.argv[1] #argv[0] = script name; server1.py
    port = int(sys.argv[2]) #argv[1] = IP, argv[2] = port

    socket_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    socket_fd.connect((addr,port)) #Pass pair (IP,port) to connect()

    #Intital check to see if server is busy
    i_response = socket_fd.recv(BUFFER_SIZE).decode()
    print("Server replied:", i_response)
    if "Error: Server busy" in i_response:
        socket_fd.close()
        sys.exit(1)

    #Create infinite loop that is only stopped with ctrl+c
    try:
        while True:
            word = input("Please enter word to be defined: ").lower()   #dictionary only has lowercase keys
            socket_fd.send(word.encode())
            
            response = socket_fd.recv(BUFFER_SIZE)
            print("Server replied - The definition(s) of " + word + ": ", response.decode())

    except KeyboardInterrupt:
        print("\nClient severing connection(forcibly closed: ctrl+c).")
        socket_fd.shutdown(socket.SHUT_WR) #Cleanly shutdown as to not cause exception that gets sent to server.
        socket_fd.close()

    print("Client finished.")
    