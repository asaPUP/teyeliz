"""
Teyeliz - Clase Client
"""

# Import Python modules
import socket
import pickle
import pygame
import time

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
            print(f"\nSe establecio coneccion con: {self.connection_address}\n")
        except ConnectionRefusedError:
            # Show a window, with the text "Server is not available.\nPress ENTER to try again..."
            font = self.pygame_data[2]

            text = font.render(
                "El servidor no esta disponible.", True, (255, 255, 255))
            text = pygame.transform.scale(
                text, (text.get_width() * 2, text.get_height() * 2))
            text2 = font.render(
                "[CUALQUIER TECLA] para reintentar...", True, (255, 255, 255))
            text2 = pygame.transform.scale(text2, (text2.get_width() * 2, text2.get_height() * 2))

            text_rect = text.get_rect()
            text_rect2 = text2.get_rect()

            text_rect.center = (380, 206)
            text_rect2.center = (380, 236)

            self.pygame_data[1].blit(text, text_rect)
            self.pygame_data[1].blit(text2, text_rect2)

            self.pygame_data[0].flip()

            print("\nEl servidor no esta disponible.")
            print("Presiona [CUALQUIER TECLA] para reintentar...\n")

            # Wait for the user to press ENTER
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

    def send_data(self, card_index, played_data):
        self.data_to_send = (card_index, played_data)
        self.data_pickle = pickle.dumps(self.data_to_send)
        self.client_socket.send(self.data_pickle)

    def receive_data(self):
        print(f"\nEsperando los datos del Servidor...\n")

        self.receive_data_helper()

        card_index, played_data = pickle.loads(self.received_data)
        print(f"\nRecibido del Servidor: index = {card_index}, data = {played_data}\n")

        return (card_index, played_data)

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

        try:
            self.client_socket.settimeout(0)
            self.received_data = self.client_socket.recv(1024)
            self.client_socket.settimeout(None)
        except:
            time.sleep(0.5)
            self.receive_data_helper()

    def close_client(self):
        self.client_socket.close()
