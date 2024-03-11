"""
Teyeliz - Menu Class
"""

# Import Python modules
import pygame

# Import game modules
from data.player import Player

# Menu class
class Menu():
    # Constructor
    def __init__(self, pygame_data):
        # Initialize the chosen socket
        self.socket = None

        # Initialize players
        self.player1 = Player(0, pygame_data)
        self.player2 = Player(1, pygame_data)

        # Receive pygame data
        self.pygame_data = pygame_data

        # Load menu background and scale it
        self.title = pygame.image.load("resources/graphics/bg/title.png")
        self.title = pygame.transform.scale(self.title, (760, 412))

        # Load logo and scale it
        self.logo = pygame.image.load("resources/graphics/logo/logo.png")
        self.logo = pygame.transform.scale(self.logo, (self.logo.get_width() * 6, self.logo.get_height() * 6))

        # Load menu icons and scale them
        self.tletl_icon = pygame.image.load("resources/graphics/icons/iconTletl.png")
        self.tletl_icon = pygame.transform.scale(self.tletl_icon, (self.tletl_icon.get_width() * 3, self.tletl_icon.get_height() * 3))

        self.atl_icon = pygame.image.load("resources/graphics/icons/iconAtl.png")
        self.atl_icon = pygame.transform.scale(self.atl_icon, (self.atl_icon.get_width() * 3, self.atl_icon.get_height() * 3))

        self.metl_icon = pygame.image.load("resources/graphics/icons/iconMetl.png")
        self.metl_icon = pygame.transform.scale(self.metl_icon, (self.metl_icon.get_width() * 3, self.metl_icon.get_height() * 3))

    # Function to show the menu
    def show_menu(self):
        # Show menu background
        self.pygame_data[1].blit(self.title, (0, 0))
        pygame.display.flip()

        # Load menu text and scale it
        font = self.pygame_data[2]
        text = font.render("Select a role", True, (255, 255, 255))
        text = pygame.transform.scale(text, (text.get_width() * 3, text.get_height() * 3))
        text2 = font.render("[1] Server", True, (255, 255, 255))
        text2 = pygame.transform.scale(text2, (text2.get_width() * 3, text2.get_height() * 3))
        text3 = font.render("[2] Client", True, (255, 255, 255))
        text3 = pygame.transform.scale(text3, (text3.get_width() * 3, text3.get_height() * 3))
        text_rect = text.get_rect()
        text_rect2 = text2.get_rect()
        text_rect3 = text3.get_rect()
        text_rect.center = (380, 300)
        text_rect2.center = (380, 340)
        text_rect3.center = (380, 380)

        # Draw a rectangle behind the text
        pygame.draw.rect(self.pygame_data[1], (0, 0, 0), (text_rect.x - 4, text_rect.y - 4, text_rect.width + 4, text_rect.height + 4), 0)
        pygame.draw.rect(self.pygame_data[1], (0, 0, 0), (text_rect2.x - 4, text_rect2.y - 4, text_rect2.width + 4, text_rect2.height + 4), 0)
        pygame.draw.rect(self.pygame_data[1], (0, 0, 0), (text_rect3.x - 4, text_rect3.y - 4, text_rect3.width + 4, text_rect3.height + 4), 0)

        self.pygame_data[1].blit(text, text_rect)
        self.pygame_data[1].blit(text2, text_rect2)
        self.pygame_data[1].blit(text3, text_rect3)

        # Load logo
        logo_rect = self.logo.get_rect()
        logo_rect.center = (380, 100)
        self.pygame_data[1].blit(self.logo, logo_rect)

        # Load menu icons
        tletl_icon_rect = self.tletl_icon.get_rect()
        tletl_icon_rect.center = (230, 220)
        self.pygame_data[1].blit(self.tletl_icon, tletl_icon_rect)

        atl_icon_rect = self.atl_icon.get_rect()
        atl_icon_rect.center = (380, 220)
        self.pygame_data[1].blit(self.atl_icon, atl_icon_rect)

        metl_icon_rect = self.metl_icon.get_rect()
        metl_icon_rect.center = (530, 220)
        self.pygame_data[1].blit(self.metl_icon, metl_icon_rect)

        # Update pygame window
        pygame.display.flip()

        # Get the selected player role
        return self.select_role()
    
    # Function to select the player role
    def select_role(self):
        # Initialize player role
        player_role = None

        # Get player selection
        pygame.event.clear()
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

         # Set the player socket type according to the selected role
        if player_role == 1:
            # Start the game as server
            print("\nStarting game as Server...\n")
            self.socket = 0
        else:
            # Start the game as client
            print("\nStarting game as Client...\n")
            self.socket = 1

        # Change menu background without text
        self.pygame_data[1].blit(self.title, (0, 0))

        # Update pygame window
        pygame.display.flip()

        return (self.player1, self.player2, self.socket)
