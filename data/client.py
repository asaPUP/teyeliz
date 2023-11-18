"""
Teyeliz - Clase Client
"""

# Import Python modules
import socket
import pickle
import pygame

# Import custom modules

class Client():
    def __init__(self, pygame_data):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_address = ('localhost', 1357)

        self.data_to_send = None
        self.data_pickle = None

        self.received_data = None

        self.pygame_data = pygame_data

    def connect_to_server(self):
        try:
            self.client_socket.connect(self.connection_address)
        except ConnectionRefusedError:
            # Show a window, with the text "Server is not available.\nPress ENTER to try again..."
            font = self.pygame_data[2]
            text = font.render("Server is not available.", True, (255, 255, 255))
            text2 = font.render("Press ENTER to try again...", True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect2 = text2.get_rect()
            text_rect.center = (380, 206)
            text_rect2.center = (380, 226)
            self.pygame_data[1].blit(text, text_rect)
            self.pygame_data[1].blit(text2, text_rect2)
            self.pygame_data[0].flip()

            print("\nServer is not available.")
            print("Press ENTER to try again...\n")

            # Wait for the user to press ENTER
            pygame.event.clear()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.connect_to_server()
                            return
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            quit()
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
    
    def send_data(self, card_index, played_data):
        self.data_to_send = (card_index, played_data)
        self.data_pickle = pickle.dumps(self.data_to_send)
        self.client_socket.send(self.data_pickle)

    def receive_data(self):
        print(f"\nWaiting for 'Server' to play a card...\n")
        self.received_data = self.client_socket.recv(1024)
        card_index, played_data = pickle.loads(self.received_data)
        return (card_index, played_data)
    
    def close_client(self):
        self.client_socket.close()