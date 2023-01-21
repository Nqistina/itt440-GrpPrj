import socket

def handle_client(client_socket):
    # Receive incoming message from client
    request = client_socket.recv(1024)

    # Manipulate the incoming message by appending "from server xyz"
    response = request + b" from server xyz"

    # Send the response back to the client
    client_socket.sendall(response)

    # Close the client socket
    client_socket.close()

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific host and port
server_socket.bind(("192.168.0.121", 8080))

# Start listening for incoming client connections
server_socket.listen()

while True:
    # Wait and accept incoming client connection
    client_socket, client_address = server_socket.accept()

    # Start a new thread to handle the incoming client request
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()

# Close the server socket
server_socket.close()