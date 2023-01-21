import socket
import threading
import time
import sys

def handle_client(client_socket):
    global stop_flag
    stop_flag = False
    # Receive incoming message from client
    request = client_socket.recv(1024)

    # Manipulate the incoming message by appending "from server xyz"
    response = request + b" from server xyz"

    # Send the response back to the client
    client_socket.sendall(response)
    time.sleep(1)
    print("\nServer responded")
    time.sleep(2)

    # Close the client socket
    client_socket.close()

    if client_socket.fileno() == -1:
        # Handle the case where the client closes the connection
        print("Client closed the connection")
        time.sleep(1)
        stop_flag = True


# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to a specific host and port
server_socket.bind(("192.168.56.102", 8080))

# Start listening for incoming client connections
server_socket.listen()
print("waiting for client connections")
for i in range(3):
    time.sleep(.5)
    sys.stdout.write('.')
    sys.stdout.flush()

while True:
    # Wait and accept incoming client connection
    client_socket, client_address = server_socket.accept()
    print("\nconnection from", client_address)
    print("waiting for client message")
    for i in range(3):
        time.sleep(.5)
        sys.stdout.write('.')
        sys.stdout.flush()

    # Create a thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
    client_thread.join()
    
    if stop_flag==True:
        break

#close the server
server_socket.close()
print("Server terminated successfully")