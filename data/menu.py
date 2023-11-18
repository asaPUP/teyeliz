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
        self.player1 = Player(0, pygame_data)
        self.player2 = Player(1, pygame_data)

        # Pyagme data = [pygame.display, window, font]
        self.pygame_data = pygame_data

        # Load the menu title screen and scale it
        self.title = pygame.image.load("resources/graphics/bg/title.png")
        self.title = pygame.transform.scale(self.title, (760, 412))

        # Load the logo and scale it


    def show_menu(self):
        # Show the menu title screen
        self.pygame_data[1].blit(self.title, (0, 0))
        pygame.display.flip()

        # Load the text "Select your role
        font = self.pygame_data[2]
        text = font.render("Select your role:", True, (255, 255, 255))
        text2 = font.render("1. Server", True, (255, 255, 255))
        text3 = font.render("2. Client", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect2 = text2.get_rect()
        text_rect3 = text3.get_rect()
        text_rect.center = (380, 206)
        text_rect2.center = (380, 226)
        text_rect3.center = (380, 246)
        self.pygame_data[1].blit(text, text_rect)
        self.pygame_data[1].blit(text2, text_rect2)
        self.pygame_data[1].blit(text3, text_rect3)

        # Update the pygame window
        pygame.display.flip()

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
            print("\nStarting the game as Server...\n")

            self.socket = 0

        else:
            # Start the game as the client
            print("\nStarting the game as Client...\n")

            self.socket = 1

        # Show the title screen without the logo or the text
        self.pygame_data[1].blit(self.title, (0, 0))
        pygame.display.flip()

        # Create the players
        return (self.player1, self.player2, self.socket)