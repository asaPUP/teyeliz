"""
Teyeliz - Main menu
"""

# Imprtamos los modulos de python
import pygame

# Importamos los modulos del juego
from data.player import Player

# Clase Menu
class Menu():
    # Constructor
    def __init__(self, pygame_data):
        # Inicializa el socket a elegir
        self.socket = None

        # Inicializa los jugadores
        self.player1 = Player(0, pygame_data)
        self.player2 = Player(1, pygame_data)

        # Recibe los datos de pygame
        self.pygame_data = pygame_data

        # Carga el fondo del menu y lo escala
        self.title = pygame.image.load("resources/graphics/bg/title.png")
        self.title = pygame.transform.scale(self.title, (760, 412))

        # Carga el logo y lo escala
        self.logo = pygame.image.load("resources/graphics/logo/logo.png")
        self.logo = pygame.transform.scale(self.logo, (self.logo.get_width() * 6, self.logo.get_height() * 6))

        # Carga los iconos del menu y los escala
        self.tletl_icon = pygame.image.load("resources/graphics/icons/iconTletl.png")
        self.tletl_icon = pygame.transform.scale(self.tletl_icon, (self.tletl_icon.get_width() * 3, self.tletl_icon.get_height() * 3))

        self.atl_icon = pygame.image.load("resources/graphics/icons/iconAtl.png")
        self.atl_icon = pygame.transform.scale(self.atl_icon, (self.atl_icon.get_width() * 3, self.atl_icon.get_height() * 3))

        self.metl_icon = pygame.image.load("resources/graphics/icons/iconMetl.png")
        self.metl_icon = pygame.transform.scale(self.metl_icon, (self.metl_icon.get_width() * 3, self.metl_icon.get_height() * 3))

    # Funcion que muestra el menu
    def show_menu(self):
        # Muestra el fondo del menu
        self.pygame_data[1].blit(self.title, (0, 0))
        pygame.display.flip()

        # Carga el texto del menu y lo escala
        font = self.pygame_data[2]
        text = font.render("Selecciona un rol", True, (255, 255, 255))
        text = pygame.transform.scale(text, (text.get_width() * 3, text.get_height() * 3))
        text2 = font.render("[1] Servidor", True, (255, 255, 255))
        text2 = pygame.transform.scale(text2, (text2.get_width() * 3, text2.get_height() * 3))
        text3 = font.render("[2] Cliente", True, (255, 255, 255))
        text3 = pygame.transform.scale(text3, (text3.get_width() * 3, text3.get_height() * 3))
        text_rect = text.get_rect()
        text_rect2 = text2.get_rect()
        text_rect3 = text3.get_rect()
        text_rect.center = (380, 300)
        text_rect2.center = (380, 340)
        text_rect3.center = (380, 380)

        # Coloca un recuadro detras del texto
        pygame.draw.rect(self.pygame_data[1], (0, 0, 0), (text_rect.x - 4, text_rect.y - 4, text_rect.width + 4, text_rect.height + 4), 0)
        pygame.draw.rect(self.pygame_data[1], (0, 0, 0), (text_rect2.x - 4, text_rect2.y - 4, text_rect2.width + 4, text_rect2.height + 4), 0)
        pygame.draw.rect(self.pygame_data[1], (0, 0, 0), (text_rect3.x - 4, text_rect3.y - 4, text_rect3.width + 4, text_rect3.height + 4), 0)

        self.pygame_data[1].blit(text, text_rect)
        self.pygame_data[1].blit(text2, text_rect2)
        self.pygame_data[1].blit(text3, text_rect3)

        # Carga el logo
        logo_rect = self.logo.get_rect()
        logo_rect.center = (380, 100)
        self.pygame_data[1].blit(self.logo, logo_rect)

        # Cargo los iconos del menu
        tletl_icon_rect = self.tletl_icon.get_rect()
        tletl_icon_rect.center = (230, 220)
        self.pygame_data[1].blit(self.tletl_icon, tletl_icon_rect)

        atl_icon_rect = self.atl_icon.get_rect()
        atl_icon_rect.center = (380, 220)
        self.pygame_data[1].blit(self.atl_icon, atl_icon_rect)

        metl_icon_rect = self.metl_icon.get_rect()
        metl_icon_rect.center = (530, 220)
        self.pygame_data[1].blit(self.metl_icon, metl_icon_rect)

        # Actualiza la ventana de pygame
        pygame.display.flip()

        # Obtiene el rol del jugador seleccionado
        return self.select_role()
    
    # Funcion que selecciona el rol del jugador
    def select_role(self):
        # Inicializa el rol del jugador
        player_role = None

        # Obtiene la seleccion del jugador
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

         # Establece el tipo de socket del jugador segun el rol seleccionado
        if player_role == 1:
            # Inicia el juego como servidor
            print("\nIniciando juego como Servidor...\n")
            self.socket = 0
        else:
            # Inicia el juego como cliente
            print("\nIniciando juego como Cliente...\n")
            self.socket = 1

        # Cambia el fondo del menu sin el texto
        self.pygame_data[1].blit(self.title, (0, 0))

        # Actualiza la ventana de pygame
        pygame.display.flip()

        return (self.player1, self.player2, self.socket)