<h2>Description</h2>
A simple client-server system, where the client is used to chat with a "dictionary" server. The protocol between the server and client first starts with the server being started on a dedicated port. Any client that wants to conncet to the server needs to know the port and IP address of the server. The server also needs access to the dictionary file. The client program is then started (using server IP and port number passed through command line). The client connects to the server then asks the user for input, the user enters a single word as input, which is then sent to the server via connected socket. The server reads the user's input from the client socket, retrieves defintion from the dictionary file, then sends the result back to the client. The client should display the server's rely to the user, prompt for the next word, until the user terminates the client using ctrl+c. This project programs 3 versions of the server:
1. Server 1 is a single process server that can handle only 1 client at a time. If a second client tries to chat with the server while one client's session is already in progress, the second client's socket operations should see an error.
2. Server 2 is a multi-process server that will “fork” a process for every new client it receives. Multiple clients should be able to simultaneously chat with the server.
3. Server 3 is a single process server that uses the "select" system call to handle multiple clients. Again, much like server2, server3 will also be able to handle multiple clients concurrently.

<h2>How to run/compile</h2>
1. Select a server you want to use, and in a terminal run:      python server1/2/3.py (port number)
2. In a separate terminal connect to your server by running:    python client.py (IP Address) (port number) 
3. If running server 2 or 3, or error checking for server 1, run in a third terminal: python client.py (IP Address) (port number) 
4. Enter into the client terminals a word to retrieve the defintion of.
5. Once finished with a client, ctrl+c to terminate, and continue with other clients if desired.
6. Once finished with the program and server, ctrl+c in the server terminal to terminate, program is finished.

<h2>Socket Project Clarifications</h2>
* Since the os.fork() Python method is only available on Unix systems, using the multiprocessing package instead is acceptable.
* Selecting sockets should use the select python library
* Socket interaction must use the socket library

<h2>General process of building a server/client connection: create, bind, listen, accept, recv, send</h2>
1. Create server socket socket_fd
2. bind() on the IP address and port we want to listen on to reserve the services
3. listen() on the IP address and port so that the socket can receive connections from clients
4. accept() a client given socket_fd by calling socket_fd.accept() so that a connection between client/server is created
5. Use the return values from accept() to retrieve data from the client using recv(), and send a response using send()

<h2>Server 1 Test Cases</h2>
1. Single client - expected result: server sends correct definitions of words
    > python client.py 127.0.0.1 5000
    Connected to server
    Please enter the word that you need defined: word1
    Server replied: definition of word1
    Please enter the word that you need defined: word 2
    Server replied: definition of word 2
    Client severing connection(forcibly closed: ctrl+c).
    Client finished.
2. Double client - expected result: server rejects second client and the second client gets an error message for busy
    > python client.py 127.0.0.1 5000
    Connected to server
    Please enter the word that you need defined: word1
    Server replied: definition of word1
    Please enter the word that you need defined: word 2
    Server replied: definition of word 2
    Client severing connection(forcibly closed: ctrl+c).
    Client finished.

    > python client.py 127.0.0.1 5000
    Server replied: Error: Server busy. Multiple clients not allowed.

<h2>Server 2 Test Cases</h2>
1. 

