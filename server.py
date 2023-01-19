import socket

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server
client_socket.connect(("localhost", 8080))

# Prompt the user to enter a message
message = input("Enter a message: ")

# Send the message to the server
client_socket.send(message)

# Receive the response from the server
response = client_socket.recv(1024)

# Print the response
print("Response from server:", response)

# Close the client socket
client_socket.close()