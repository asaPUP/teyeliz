"""
Teyeliz - Clase Server
"""

# Import Python modules
import socket
import pickle
import pygame
import time

# Server class
class Server():
    # Constructor
    def __init__(self, pygame_data):
        # Initialize the server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP

        self.ip_address = socket.gethostbyname(socket.gethostname())  # Server IP address

        self.binding_address = (self.ip_address, 7777)  # Server address to bind

        # Connection data
        self.connection = None
        self.address = None

        # Data to send to the client and its pickle (serialization)
        self.data_to_send = None
        self.data_pickle = None

        # Data received from the client
        self.received_data = None

        # Receive pygame data
        self.pygame_data = pygame_data

    # Function to start the server
    def start_server(self):
        # Set the server socket as reusable, so the server can be restarted without waiting for the port to be released
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the server socket to the server address
        self.server_socket.bind(self.binding_address)
        self.server_socket.listen(1)

        # Print a message to the console
        print("\nWaiting for the Client to connect...\n")

        # Wait for the client to connect
        self.wait_for_client()

    # Function to wait for the client to connect
    def wait_for_client(self):
        # Display a message on the pygame screen
        font = self.pygame_data[2]
        text = font.render("Waiting for the Client to connect...", True, (255, 255, 255))
        text = pygame.transform.scale(text, (text.get_width() * 2, text.get_height() * 2))
        text_rect = text.get_rect()
        text_rect.center = (380, 206)
        self.pygame_data[1].blit(text, text_rect)
        self.pygame_data[0].flip()

        # Check pygame events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.server_socket.close()
                    pygame.quit()
                    quit()
            if event.type == pygame.QUIT:
                self.server_socket.close()
                pygame.quit()
                quit()

        try:  # Try to accept the client's connection without blocking the program (timeout = 0)
            self.server_socket.settimeout(0)
            self.connection, self.address = self.server_socket.accept()
            self.server_socket.settimeout(None)
            print(f"\nConnection established with: {self.address}\n")
            pygame.event.clear()
            return
        except:  # If unable to connect to the client, retry the connection after 0.5 seconds
            time.sleep(0.5)
            self.wait_for_client()

    # Function to send data to the client
    def send_data(self, card_index, played_data):
        self.data_to_send = (card_index, played_data)
        self.data_pickle = pickle.dumps(self.data_to_send)
        self.connection.send(self.data_pickle)

    # Function to receive data of the card played by the client
    def receive_data(self):
        # Print a message to the console
        print(f"\nWaiting for data from the Client...\n")

        # Display a message on the pygame screen
        self.receive_data_helper()

        # Deserialize the received data
        card_index, played_data = pickle.loads(self.received_data)
        print(f"\nReceived from the Client: index = {card_index}, data = {played_data}\n")

        return (card_index, played_data)

    # Helper function to receive data from the client
    def receive_data_helper(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.connection.close()
                    self.server_socket.close()
                    pygame.quit()
                    quit()
            if event.type == pygame.QUIT:
                self.connection.close()
                self.server_socket.close()
                pygame.quit()
                quit()

        try:  # Try to receive data from the client
            self.server_socket.settimeout(0)
            self.received_data = self.connection.recv(1024)
            self.server_socket.settimeout(None)
        except:  # If data from the client is not received, try again after 0.5 seconds
            time.sleep(0.5)
            self.receive_data_helper()

    # Function to close the server socket
    def close_server(self):
        self.connection.close()
        self.server_socket.close()
