"""
Teyeliz - Clase Server
"""

# Importamos los modulos de python
import socket
import pickle
import pygame
import time

# Clase Server
class Server():
    # Constructor
    def __init__(self, pygame_data):
        # Inicializa el socket del servidor
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET = IPv4, SOCK_STREAM = TCP

        self.ip_address = socket.gethostbyname(socket.gethostname()) # Direccion IP del servidor

        self.binding_address = (self.ip_address, 7777) # Direccion del servidor a enlazar

        # Datos de la conexion
        self.connection = None
        self.address = None

        # Datos a enviar al cliente y su pickle (serializacion)
        self.data_to_send = None
        self.data_pickle = None

        # Datos recibidos del cliente
        self.received_data = None

        # Recibe los datos de pygame
        self.pygame_data = pygame_data

    # Funcion que inicia el servidor
    def start_server(self):
        # Establece el socket del servidor como reutilizable, para que se pueda reiniciar el servidor sin esperar a que el puerto se libere
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Enlaza el socket del servidor a la direccion del servidor
        self.server_socket.bind(self.binding_address)
        self.server_socket.listen(1)

        # Imprime un mensaje en la consola
        print("\nEsperando a que el Cliente se conecte...\n")

        # Espera a que el cliente se conecte
        self.wait_for_client()

    # Funcion que espera a que el cliente se conecte
    def wait_for_client(self):
        # Muestra un mensaje en la pantalla de pygame
        font = self.pygame_data[2]
        text = font.render("Esperando a que el Cliente se conecte...", True, (255, 255, 255))
        text = pygame.transform.scale(text, (text.get_width() * 2, text.get_height() * 2))
        text_rect = text.get_rect()
        text_rect.center = (380, 206)
        self.pygame_data[1].blit(text, text_rect)
        self.pygame_data[0].flip()

        # Detecta los eventos de pygame
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

        try: # Intenta aceptar la conexion del cliente sin bloquear el programa (timeout = 0)
            self.server_socket.settimeout(0)
            self.connection, self.address = self.server_socket.accept()
            self.server_socket.settimeout(None)
            print(f"\nSe establecio coneccion con: {self.address}\n")
            pygame.event.clear()
            return
        except: # Si no se puede conectar al cliente reintenta la conexion tras 0.5 segundos
            time.sleep(0.5)
            self.wait_for_client()

    # Funcion que envia los datos al cliente
    def send_data(self, card_index, played_data):
        self.data_to_send = (card_index, played_data)
        self.data_pickle = pickle.dumps(self.data_to_send)
        self.connection.send(self.data_pickle)

    # Funcion que recibe los datos de la carta jugada por el cliente
    def receive_data(self):
        # Imprime un mensaje en la consola
        print(f"\nEsperando los datos del Cliente...\n")

        # Muestra un mensaje en la pantalla de pygame
        self.receive_data_helper()

        # Deserializa los datos recibidos
        card_index, played_data = pickle.loads(self.received_data)
        print(f"\nRecibido del Cliente: index = {card_index}, data = {played_data}\n")

        return (card_index, played_data)

    # Funcion auxiliar que recibe los datos del cliente
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

        try: # Intenta recibir los datos del cliente
            self.server_socket.settimeout(0)
            self.received_data = self.connection.recv(1024)
            self.server_socket.settimeout(None)
        except: # Si no se reciben los datos del cliente se intenta de nuevo tras 0.5 segundos
            time.sleep(0.5)
            self.receive_data_helper()

    # Funcion que cierra el socket del servidor
    def close_server(self):
        self.connection.close()
        self.server_socket.close()
