"""
Teyetest - Main menu
Select if the player is the server or the client
and start the game accordingly
"""

# Import Python modules
# import pygame

# Import custom modules
from player import Player

class Menu():
    def __init__(self):
        self.socket = None
        self.player1 = Player(0)
        self.player2 = Player(1)

    def show_menu(self):
        # Select if the player is the server or the client
        print("Select your role:")
        print("1. Server")
        print("2. Client")

        # Get the player role
        while True:
            try:
                player_role = int(input("Enter your choice: "))
                if player_role > 0 and player_role < 3:
                    break
            except ValueError:
                pass   

        # Start the game in the selected role
        if player_role == 1:
            # Start the game as the server
            print("Starting the game as Server...")

            self.socket = 0
        else:
            # Start the game as the client
            print("Starting the game as Client...")

            self.socket = 1

        # Create the players

        return (self.player1, self.player2, self.socket)