import socket
import time
import sys

print("Connecting to server")
for i in range(3):
    time.sleep(.5)
    sys.stdout.write('.')
    sys.stdout.flush()

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server
client_socket.connect(("192.168.56.102", 8080))
print("\nConnected to server!")
time.sleep(1)

# Prompt the user to enter a message
message = input("Enter a message: ")

# Send the message to the server
client_socket.sendall(message.encode())

# Receive the response from the server
response = client_socket.recv(1024)
print("Waiting for response")
for i in range(3):
    time.sleep(.5)
    sys.stdout.write('.')
    sys.stdout.flush()

# Print the response
print("\nResponse from server:", response.decode())

# Close the client socket
client_socket.close()
time.sleep(1)
print("Client Terminated")
