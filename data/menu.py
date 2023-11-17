"""
Teyeliz - Main menu
"""

# Import Python modules
import pygame

# Import custom modules
from data.player import Player

class Menu():
    def __init__(self, pygame_data):
        self.socket = None
        self.player1 = Player(0)
        self.player2 = Player(1)

        # Pyagme data = [pygame.display, window, font]
        self.pygame_data = pygame_data

        # Load the menu title screen and scale it
        self.title = pygame.image.load("resources/graphics/bg/title.png")
        self.title = pygame.transform.scale(self.title, (760, 412))

    def show_menu(self):
        # Show the menu title screen
        self.pygame_data[1].blit(self.title, (0, 0))
        pygame.display.flip()

        # Select if the player is the server or the client from the menu pygame screen
        print("Select your role:")
        print("1. Server")
        print("2. Client")

        # Get the player role from the menu pygame screen instead of the console
        pygame.event.clear()

        player_role = None
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        player_role = 1
                        break
                    elif event.key == pygame.K_2:
                        player_role = 2
                        break
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            if player_role == 1 or player_role == 2:
                break

        # Start the game in the selected role
        if player_role == 1:
            # Start the game as the server
            print("Selected role 1")
            print("Starting the game as Server...")

            self.socket = 0

        else:
            # Start the game as the client
            print("Selected role 2")
            print("Starting the game as Client...")

            self.socket = 1

        # Create the players
        return (self.player1, self.player2, self.socket)