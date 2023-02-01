#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <sys/wait.h>
#include <signal.h>

int server_socket;
void interrupt_handler(int signal) {
  printf("\n Closing server socket...\n");
  close(server_socket);
  exit(0);
}

void process_connection(int client_socket) {
char client_message[1000];
char server_message[2000];

// Receive incoming text from the client
int recv_size = recv(client_socket, client_message, 1000, 0);
if (recv_size == -1) {
    perror("Receive failed");
    return;
}
client_message[recv_size] = '\0';

// Manipulate the incoming text stream
sprintf(server_message, "%s from server xyz", client_message);

// Send the combined string back to the client
if (send(client_socket, server_message, strlen(server_message), 0) < 0) {
    perror("Send failed");
    return;
}

// Close the client socket
close(client_socket);
}

int main(int argc, char *argv[]) {
int server_socket, client_socket;
struct sockaddr_in server, client;

// Create the server socket
server_socket = socket(AF_INET, SOCK_STREAM, 0);
if (server_socket == -1) {
    printf("Could not create server socket");
    return 1;
}
printf("Server socket created\n");

// Fill in the server information`
server.sin_family = AF_INET;
server.sin_addr.s_addr = INADDR_ANY;
server.sin_port = htons(8080);

// Bind the socket to the specified port and address
if (bind(server_socket, (struct sockaddr *) &server, sizeof(server)) < 0) {
    perror("Bind failed");
    return 1;
}
printf("Bind Success\n");

// Start listening for incoming connections
listen(server_socket, 5);
printf("Waiting for incoming connections...\n");

// Register the interrupt handler
signal(SIGINT, interrupt_handler);

// Accept incoming connections
while (1) {
    int c = sizeof(struct sockaddr_in);
    client_socket = accept(server_socket, (struct sockaddr *) &client, (socklen_t *) &c);
    if (client_socket < 0) {
        perror("Accept failed");
        return 1;
    }
    printf("Accepted connection from client: %s\n", inet_ntoa(client.sin_addr));

    // Handle incoming connection in a separate process using fork
    int pid = fork();
    if (pid == 0) {
        // Child process
        close(server_socket);
        process_connection(client_socket);
        exit(0);
    } else {
        // Parent process
        close(client_socket);
    }
}

// Close the server socket
close(server_socket);

return 0;
}