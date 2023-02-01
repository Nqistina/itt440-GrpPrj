#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    int sock;
    struct sockaddr_in server;
    char message[1000], server_reply[2000];

    // Create the socket
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1) {
        printf("Could not create socket");
        return 1;
    }
    printf("Socket created\n");

    // Fill in the server information
    server.sin_addr.s_addr = inet_addr("192.168.56.102");
    server.sin_family = AF_INET;
    server.sin_port = htons(8080);

    // Connect to the server
    if (connect(sock, (struct sockaddr *) &server, sizeof(server)) < 0) {
        perror("Connect failed. Error");
        return 1;
    }
    printf("Connected to server\n");

    // Compose a string from user input
    printf("Enter a message: ");
    fgets(message, 1000, stdin);

    // Send the message to the server
    if (send(sock, message, strlen(message), 0) < 0) {
        perror("Send failed");
        return 1;
    }
    printf("Data sent\n");

    // Receive the response from the server
    int recv_size = recv(sock, server_reply, 2000, 0);
    if (recv_size == -1) {
        perror("Receive failed");
        return 1;
    }
    server_reply[recv_size] = '\0';

    // Print the response from the server
    printf("Response from server: %s\n", server_reply);

    // Close the socket
    close(sock);

    return 0;
}
