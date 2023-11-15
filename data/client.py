"""
Teyetest - Clase Client
"""

# Import Python modules
import socket
import pickle

class Client():
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_address = ('localhost', 1357)

        self.data_to_send = None
        self.data_pickle = None

        self.received_data = None

    def connect_to_server(self):
        while True:
            try:
                self.client_socket.connect(self.connection_address)
                break
            except ConnectionRefusedError:
                print("\nServer is not available.")
                input("Press ENTER to try again...\n")
                pass
    
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