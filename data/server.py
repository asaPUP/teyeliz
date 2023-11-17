"""
Teyeliz - Clase Server
"""

# Import Python modules
import socket
import pickle
import pygame

# Import custom modules

# Server class
class Server():
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.binding_address = ('localhost', 1357)

        self.connection = None
        self.address = None

        self.data_to_send = None
        self.data_pickle = None
         
        self.received_data = None

    def start_server(self):
        self.server_socket.bind(self.binding_address)
        self.server_socket.listen(1)

        print("\nWaiting for Client to connect...\n")
        self.connection, self.address = self.server_socket.accept()
        print(f"\nConnection from {self.address} has been established.\n")

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