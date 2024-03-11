"""
Teyeliz - Client Class
"""

# Import Python modules
import socket
import pickle
import pygame
import time

# Client class
class Client():
    # Constructor
    def __init__(self, pygame_data):
        # Initialize the client socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP

        self.ip_address = socket.gethostbyname(socket.gethostname())  # Client's IP address

        self.connection_address = (self.ip_address, 7777)  # Server's address to connect to

        # Data to send to the server and its pickle (serialization)
        self.data_to_send = None
        self.data_pickle = None

        # Data received from the server
        self.received_data = None

        # Receive pygame data
        self.pygame_data = pygame_data

    # Function to connect the client to the server
    def connect_to_server(self):
        try:  # Attempt to connect to the server
            self.client_socket.connect(self.connection_address)
            print(f"\nConnection established with: {self.connection_address}\n")
        except ConnectionRefusedError:  # If unable to connect to the server, retry connection
            # Display an error message on the pygame screen
            font = self.pygame_data[2]

            text = font.render("The server is not available.", True, (255, 255, 255))
            text = pygame.transform.scale(text, (text.get_width() * 2, text.get_height() * 2))
            text2 = font.render("[ANY KEY] to retry...", True, (255, 255, 255))
            text2 = pygame.transform.scale(text2, (text2.get_width() * 2, text2.get_height() * 2))

            text_rect = text.get_rect()
            text_rect2 = text2.get_rect()

            text_rect.center = (380, 206)
            text_rect2.center = (380, 236)

            self.pygame_data[1].blit(text, text_rect)
            self.pygame_data[1].blit(text2, text_rect2)

            # Update the pygame screen
            self.pygame_data[0].flip()

            # Print a message in the console
            print("\nThe server is not available.")
            print("Press [ANY KEY] to retry...\n")

            # Wait for the user to press [ANY KEY] to retry
            pygame.event.clear()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            quit()
                        else:
                            self.connect_to_server()
                            return
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

    # Function to send played card data to the server
    def send_data(self, card_index, played_data):
        self.data_to_send = (card_index, played_data)
        self.data_pickle = pickle.dumps(self.data_to_send)
        self.client_socket.send(self.data_pickle)

    # Function to receive played card data from the server
    def receive_data(self):
        # Print a message in the console
        print(f"\nWaiting for data from the Server...\n")

        # Receive data from the server
        self.receive_data_helper()

        # Deserialize received data
        card_index, played_data = pickle.loads(self.received_data)
        print(f"\nReceived from the Server: index = {card_index}, data = {played_data}\n")

        return (card_index, played_data)

    # Auxiliary function to receive data from the server
    def receive_data_helper(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.client_socket.close()
                    pygame.quit()
                    quit()
            if event.type == pygame.QUIT:
                self.client_socket.close()
                pygame.quit()
                quit()

        try:  # Attempt to receive data from the server
            self.client_socket.settimeout(0)
            self.received_data = self.client_socket.recv(1024)
            self.client_socket.settimeout(None)
        except:  # If data from the server is not received, attempt again after 0.5 seconds
            time.sleep(0.5)
            self.receive_data_helper()

    # Function to close the client socket
    def close_client(self):
        self.client_socket.close()