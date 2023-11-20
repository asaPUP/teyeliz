"""
Teyeliz - Clase Game
"""

# Importamos los modulos de python
import pygame
import time

# Importamos los modulos del juego
from data.card import Card

# Clase Game
class Game():
    # Constructor
    def __init__(self, p1, p2, pygame_data):
        # Crea los jugadores
        self.player1 = p1
        self.player2 = p2

        # Crea las variables de las cartas jugadas
        self.played_data1 = None
        self.played_data2 = None

        # Crea la variable del numero de ronda
        self.num_round = 1

        # Carga el fondo del juego y escalarlo
        self.background = pygame.image.load("resources/graphics/bg/background.png")
        self.background = pygame.transform.scale(self.background, (760, 412))

        # Carga la pantalla de fin de juego y escalarlo
        self.game_over = pygame.image.load("resources/graphics/bg/over.png")
        self.game_over = pygame.transform.scale(self.game_over, (760, 412))

        # Carga el logo del juego
        self.logo = pygame.image.load("resources/graphics/logo/logo.png")

        # Recibe los datos de pygame
        self.pygame_data = pygame_data

    # Funcion para seleccionar una carta
    def select_card(self, player):
        # Vaciamos la cola de eventos
        pygame.event.clear()

        # Espera a que el jugador presione una tecla del 1 al 5 para seleccionar una carta
        card_index = None
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        card_index = 0
                        break
                    elif event.key == pygame.K_2:
                        card_index = 1
                        break
                    elif event.key == pygame.K_3:
                        card_index = 2
                        break
                    elif event.key == pygame.K_4:
                        card_index = 3
                        break
                    elif event.key == pygame.K_5:
                        card_index = 4
                        break
                    elif event.key == pygame.K_ESCAPE:
                        self.quit_game()
                elif event.type == pygame.QUIT:
                    self.quit_game()
            
            # Si el jugador selecciono una carta, sale del bucle
            if card_index is not None:
                break
        
        # Juega la carta seleccionada
        if player == self.player1:
            self.played_data1 = player.play_card(card_index)
            self.show_played_card(player, self.played_data1)
            return (card_index, self.played_data1)
        else:
            self.played_data2 = player.play_card(card_index)
            self.show_played_card(player, self.played_data2)
            return (card_index, self.played_data2)
    
    # Funcion para mostrar la carta jugada
    def show_played_card(self, player, data):
        # Convierte los datos de la carta en un objeto Card
        card = self.data_to_card(data)

        # Carga la imagen correspondiente a la carta jugada
        card_image = card.image
        card_image = pygame.transform.scale(card_image, (96, 156))
        card_image_rect = card_image.get_rect()

        # Muestra la carta en la ventana de pygame
        if player == self.player1:
            card_image_rect.topleft = (254, 60)
        else:
            card_image_rect.topleft = (410, 60)
        self.pygame_data[1].blit(card_image, card_image_rect)

        # Actualiza la ventana de pygame
        self.pygame_data[0].flip()

    # Funcion para convertir los datos de la carta en un objeto Card
    def data_to_card(self, data):
        element = data[0]
        color = data[1]
        power = data[2]

        return Card(element, color, power)

    # Funcion para comparar las cartas jugadas
    def compare_cards(self, data1, data2):
        # Guarda los datos de las cartas jugadas
        self.played_data1 = data1
        self.played_data2 = data2

        # Muestra las cartas jugadas en la ventana de pygame
        self.show_played_card(self.player1, data1)
        self.show_played_card(self.player2, data2)

        # Espera 1 segundo
        time.sleep(1)

        # Carga el texto de comparacion y lo escala
        font = self.pygame_data[2]
        draw_text = font.render("=", True, (255, 255, 255))
        draw_text = pygame.transform.scale(draw_text, (draw_text.get_width() * 5, draw_text.get_height() * 5))
        left_text = font.render(">", True, (255, 255, 255))
        left_text = pygame.transform.scale(left_text, (left_text.get_width() * 5, left_text.get_height() * 5))
        right_text = font.render("<", True, (255, 255, 255))
        right_text = pygame.transform.scale(right_text, (right_text.get_width() * 5, right_text.get_height() * 5))
        position = (384, 150)

        # Compara las cartas jugadas y retorna el ganador de la ronda
        if self.played_data1[0] == self.played_data2[0]: # Mismo elemento
            if self.played_data1[-1] == self.played_data2[-1]: # Mismo poder
                # Muestra un "=" en el medio de la ventana de pygame
                text = draw_text
                text_rect = text.get_rect()
                text_rect.center = position
                self.pygame_data[1].blit(text, text_rect)
                self.pygame_data[0].flip()

                time.sleep(2)

                return 0
            
            elif self.played_data1[-1] > self.played_data2[-1]: # Mayor poder
                # Muetsra un ">" en el medio de la ventana de pygame
                text = left_text
                text_rect = text.get_rect()
                text_rect.center = position
                self.pygame_data[1].blit(text, text_rect)
                self.pygame_data[0].flip()

                time.sleep(2)

                return 1
            
            else: # Menor poder
                # Muetsra un "<" en el medio de la ventana de pygame
                text = right_text
                text_rect = text.get_rect()
                text_rect.center = position
                self.pygame_data[1].blit(text, text_rect)
                self.pygame_data[0].flip()

                time.sleep(2)

                return 2
        
        # Diferente elemento
        elif ((self.played_data1[0] == 1 and self.played_data2[0] == 3) or # Tletl > Metl
              (self.played_data1[0] == 2 and self.played_data2[0] == 1) or # Atl > Tletl
              (self.played_data1[0] == 3 and self.played_data2[0] == 2)): # Metl > Atl
            
            # Muetsra un ">" en el medio de la ventana de pygame
            text = left_text
            text_rect = text.get_rect()
            text_rect.center = position
            self.pygame_data[1].blit(text, text_rect)
            self.pygame_data[0].flip()

            time.sleep(2)

            return 1
        
        else: # Caso contrario
            # Muetsra un "<" en el medio de la ventana de pygame
            text = right_text
            text_rect = text.get_rect()
            text_rect.center = position
            self.pygame_data[1].blit(text, text_rect)
            self.pygame_data[0].flip()

            time.sleep(2)

            return 2
    
    # Funcion para mostrar el resultado de la ronda
    def win_round(self, round_winner):
        if round_winner == 0:
            pass # No pasa nada
        elif round_winner == 1: # Gana el jugador 1
            self.player1.add_card_to_tictactoe(self.played_data1)
        else: # Gana el jugador 2
            self.player2.add_card_to_tictactoe(self.played_data2)
        
        # Muestra el HUD de ambos jugadores
        self.player1.show_tictactoe()
        self.player2.show_tictactoe()
    
    # Funcion para mostrar el HUD del juego
    def show_hud(self, player = None):
        # Muestra el fondo del juego
        self.pygame_data[1].blit(self.background, (0, 0))

        # Muestra el numero de ronda
        font = self.pygame_data[2]
        text = font.render(f"{self.num_round}", True, (255, 255, 255))
        text_ronda = font.render("RONDA", True, (255, 255, 255))

        # Reeescala el texto y lo muestra en la ventana de pygame
        text = pygame.transform.scale(text, (text.get_width() * 2, text.get_height() * 2))
        text_rect = text.get_rect()
        text_rect.center = (380, 26)
        self.pygame_data[1].blit(text, text_rect)

        text_ronda = pygame.transform.scale(text_ronda, (text_ronda.get_width() * 0.8, text_ronda.get_height() * 0.8))
        text_rect_ronda = text_ronda.get_rect()
        text_rect_ronda.center = (380, 10)
        self.pygame_data[1].blit(text_ronda, text_rect_ronda)

        # Muestra "TU" y "OPONENTE en la ventana de pygame segun sea el caso
        text_tu = font.render("TU", True, (255, 255, 255))
        text_tu = pygame.transform.scale(text_tu, (text_tu.get_width() * 2, text_tu.get_height() * 2))
        text_rect_tu = text_tu.get_rect()

        text_oponente = font.render("OPONENTE", True, (255, 255, 255))
        text_oponente = pygame.transform.scale(text_oponente, (text_oponente.get_width() * 2, text_oponente.get_height() * 2))
        text_rect_oponente = text_oponente.get_rect()

        if player == self.player1:
            text_rect_tu.center = (140, 48)
            self.pygame_data[1].blit(text_tu, text_rect_tu)
            text_rect_oponente.center = (620, 48)
            self.pygame_data[1].blit(text_oponente, text_rect_oponente)
        elif player == self.player2:
            text_rect_tu.center = (620, 48)
            self.pygame_data[1].blit(text_tu, text_rect_tu)
            text_rect_oponente.center = (140, 48)
            self.pygame_data[1].blit(text_oponente, text_rect_oponente)

        # Muestra el logo del juego
        logo_rect = self.logo.get_rect()
        logo_rect.center = (380, 395)
        self.pygame_data[1].blit(self.logo, logo_rect)

        # Muestra la cuadricula de cada jugador
        self.player1.show_tictactoe()
        self.player2.show_tictactoe()

        # Muetsra la mano de cada jugador
        if player == self.player1:
            self.player1.show_hand()
        elif player == self.player2:
            self.player2.show_hand()

        # Actualiza la ventana de pygame
        self.pygame_data[0].flip()

    # Funcion para retornar el ganador de la partida
    def check_winner(self):
        if self.player1.check_tictactoe():
            return 1
        elif self.player2.check_tictactoe():
            return 2
        else:
            return 0 # No hay ganador

    # Funcion para mostrar la pantalla de fin de juego
    def win_game(self, game_winner, player):
        # Muestra la pantalla de fin de juego
        self.pygame_data[1].blit(self.game_over, (0, 0))

        # Muestra un mensaje dependiendo de quien gano la partida
        if game_winner == player:
            text = self.pygame_data[2].render("GANASTE!", True, (255, 255, 255))
            text = pygame.transform.scale(text, (text.get_width() * 3, text.get_height() * 3))
        else:
            text = self.pygame_data[2].render("PERDISTE!", True, (255, 255, 255))
            text = pygame.transform.scale(text, (text.get_width() * 3, text.get_height() * 3))
        
        text2 = self.pygame_data[2].render("[CUALQUIER TECLA] para cerrar...", True, (255, 255, 255))
        text2 = pygame.transform.scale(text2, (text2.get_width() * 2, text2.get_height() * 2))
        
        text_rect = text.get_rect()
        text_rect.center = (380, 250)
        text_rect2 = text2.get_rect()
        text_rect2.center = (380, 300)
        self.pygame_data[1].blit(text, text_rect)
        self.pygame_data[1].blit(text2, text_rect2)

        # Actualiza la ventana de pygame
        self.pygame_data[0].flip()

    # Funcion para crear una nueva ronda
    def new_round(self, card_index1, card_index2):
        # Agrega una carta a la mano de cada jugador
        self.player1.draw_card(card_index1)
        self.player2.draw_card(card_index2)

        self.num_round += 1 # Aumenta el numero de ronda en 1
    
    # Funcion para cerrar el juego
    def quit_game(self):
        pygame.quit()
        quit()