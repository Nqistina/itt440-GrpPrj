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

try:
    # Connect the socket to the server
    client_socket.connect(("192.168.56.102", 8080))
    print("\nConnected to server!")

    # Prompt the user to enter a message
    message = input("Enter a message: ")

    # Send the message to the server
    client_socket.sendall(message.encode())

    # Receive the response from the server
    response = client_socket.recv(1024)

    # Print the response
    print("\nResponse from server:", response.decode())

#error handling for connection failure
except socket.error as error:
    print("\nFailed to connect to server:", error)

finally:
    # Close the client socket
    client_socket.close()
    time.sleep(1)
    print("Client Terminated")
