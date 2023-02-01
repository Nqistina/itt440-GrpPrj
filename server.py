import socket
import threading
import time
import sys
import signal


# Close server socket on keyboard interrupt
def signal_handler(sig, frame):
    print("\n Closing server socket...")
    server_socket.close()
    sys.exit(0)

# Register the signal handler to be called on keyboard interrupt
signal.signal(signal.SIGINT, signal_handler)

def handle_client(client_socket):
    # Receive incoming message from client
    request = client_socket.recv(1024)

    # Manipulate the incoming message by appending "from server xyz"
    response = request + b" from server xyz"

    # Send the response back to the client
    client_socket.sendall(response)
    time.sleep(1)
    print("Server responded \n")
   
    # Close the client socket
    client_socket.close()

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Avoid the TIME_WAIT state when the current listening process terminates
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
    
    # Create a thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()