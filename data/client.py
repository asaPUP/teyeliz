"""
Teyeliz - Clase Client
"""

# Importamos los modulos de python
import socket
import pickle
import pygame
import time

# Clase Client
class Client():
    # Constructor
    def __init__(self, pygame_data):
        # Inicializa el socket del cliente
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET = IPv4, SOCK_STREAM = TCP
        self.connection_address = ('localhost', 1357) # Direccion del servidor a conectarse

        # Datos a enviar al servidor y su pickle (serializacion)
        self.data_to_send = None
        self.data_pickle = None

        # Datos recibidos del servidor
        self.received_data = None

        # Recibe los datos de pygame
        self.pygame_data = pygame_data

    # Funcion que conecta al cliente con el servidor
    def connect_to_server(self):
        try: # Intenta conectarse al servidor
            self.client_socket.connect(self.connection_address)
            print(f"\nSe establecio coneccion con: {self.connection_address}\n")
        except ConnectionRefusedError: # Si no se puede conectar al servidor reintenta la conexion
            # Muestra un mensaje de error en la pantalla de pygame
            font = self.pygame_data[2]

            text = font.render("El servidor no esta disponible.", True, (255, 255, 255))
            text = pygame.transform.scale(text, (text.get_width() * 2, text.get_height() * 2))
            text2 = font.render("[CUALQUIER TECLA] para reintentar...", True, (255, 255, 255))
            text2 = pygame.transform.scale(text2, (text2.get_width() * 2, text2.get_height() * 2))

            text_rect = text.get_rect()
            text_rect2 = text2.get_rect()

            text_rect.center = (380, 206)
            text_rect2.center = (380, 236)

            self.pygame_data[1].blit(text, text_rect)
            self.pygame_data[1].blit(text2, text_rect2)

            # Actualiza la pantalla de pygame
            self.pygame_data[0].flip()

            # Imprime un mensaje en la consola
            print("\nEl servidor no esta disponible.")
            print("Presiona [CUALQUIER TECLA] para reintentar...\n")

            # Espera a que el usuario presione [CUALQUIER TECLA] para reintentar
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

    # Funcion que envia los datos de la carta jugada al servidor
    def send_data(self, card_index, played_data):
        self.data_to_send = (card_index, played_data)
        self.data_pickle = pickle.dumps(self.data_to_send)
        self.client_socket.send(self.data_pickle)

    # Funcion que recibe los datos de la carta jugada por el servidor
    def receive_data(self):
        # Imprime un mensaje en la consola
        print(f"\nEsperando los datos del Servidor...\n")

        # Recibe los datos del servidor
        self.receive_data_helper()

        # Deserializa los datos recibidos
        card_index, played_data = pickle.loads(self.received_data)
        print(f"\nRecibido del Servidor: index = {card_index}, data = {played_data}\n")

        return (card_index, played_data)

    # Funcion auxiliar que recibe los datos del servidor
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

        try: # Intenta recibir los datos del servidor
            self.client_socket.settimeout(0)
            self.received_data = self.client_socket.recv(1024)
            self.client_socket.settimeout(None)
        except: # Si no se reciben los datos del servidor se intenta de nuevo tras 0.5 segundos
            time.sleep(0.5)
            self.receive_data_helper()

    # Funcion que cierra el socket del cliente
    def close_client(self):
        self.client_socket.close()
