"""
Teyeliz - Clase Server
"""

# Import Python modules
import socket
import pickle
import pygame
import time

# Import custom modules

# Server class
class Server():
    def __init__(self, pygame_data):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.binding_address = ('localhost', 1357)

        self.connection = None
        self.address = None

        self.data_to_send = None
        self.data_pickle = None
         
        self.received_data = None

        self.pygame_data = pygame_data

    def start_server(self):
        # Set socket options
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the server socket to the binding address
        self.server_socket.bind(self.binding_address)
        self.server_socket.listen(1)

        # Show a window, with the text "Waiting for Client to connect..."
        font = self.pygame_data[2]
        text = font.render("Waiting for Client to connect...", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (380, 206)
        self.pygame_data[1].blit(text, text_rect)
        self.pygame_data[0].flip()

        # Non blocking accept so pygame can still run
        self.server_socket.setblocking(False)

        self.wait_for_client()
    
    def wait_for_client(self):
        # Show a window, with the text "Waiting for Client to connect..."
        font = self.pygame_data[2]
        text = font.render("Waiting for Client to connect...", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (380, 206)
        self.pygame_data[1].blit(text, text_rect)
        self.pygame_data[0].flip()

        # Non blocking accept so pygame can still run
        self.server_socket.setblocking(False)

        print("\nWaiting for Client to connect...\n")

        # Wait for the client to connect
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

        try:
            self.connection, self.address = self.server_socket.accept()
            print(f"\nConnection from {self.address} has been established.\n")
            pygame.event.clear()
            return
        except:
            time.sleep(0.5)
            self.wait_for_client()

    def send_data(self, card_index, played_data):
        self.data_to_send = (card_index, played_data)
        self.data_pickle = pickle.dumps(self.data_to_send)
        self.connection.send(self.data_pickle)

    def receive_data(self):
        print(f"\nWaiting for 'Client' to play a card...\n")
        self.received_data = self.connection.recv(1024)
        card_index, played_data = pickle.loads(self.received_data)
        return (card_index, played_data)

    def close_server(self):
        self.connection.close()
        self.server_socket.close()