"""
Teyeliz - Un juego de cartas para dos juadores con websockets TCP y pygame
"""

# Importamos los modulos de python
import pygame
from pygame.locals import *
import time

# Importamos los modulos del juego
from data.menu import Menu
from data.game import Game
from data.server import Server
from data.client import Client

# Funcion que ejecuta el juego
def play_game(player, send_data_func, receive_data_func):
    # Ciclo principal del juego
    while True:
        # Captura los eventos del teclado
        pygame.event.clear()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if player == player1:
                        server.close_server()
                    else:
                        client.close_client()
                    game.quit_game()
            if event.type == pygame.QUIT:
                if player == player1:
                    server.close_server()
                else:
                    client.close_client()
                game.quit_game()

        # El jugador selecciona una carta y la juega
        game.show_hud(player) # Muestra el HUD del jugador
        card_index1, played_data1 = game.select_card(player)

        # Envía los datos al oponente
        send_data_func(card_index1, played_data1)

        # Recibe los datos del oponente
        card_index2, played_data2 = receive_data_func()

        # Revisa cual jugador gana la ronda
        if player == player1: # Si el jugador es el servidor (player1)
            round_winner = game.compare_cards(played_data1, played_data2)
        else: # Si el jugador es el cliente (player2)
            round_winner = game.compare_cards(played_data2, played_data1)

        # Muestra el resultado de la ronda
        game.win_round(round_winner)

        # Revisa si hay un ganador de la partida y si es asi, termina el juego
        game_winner = game.check_winner()
        if game_winner > 0:
            break

        # Crea una nueva ronda
        if player == player1: # Si player es server (player1)
            game.new_round(card_index1, card_index2)
        else: # Si player es client (player2)
            game.new_round(card_index2, card_index1)

    # Encierra la cuadricula del ganador en un cuadro blanco
    if game_winner == 1:
        pygame.draw.rect(window, (255, 255, 255), (62, 62, 154, 154), 5)
        pygame.display.flip()
    else:
        pygame.draw.rect(window, (255, 255, 255), (544, 62, 154, 154), 5)
        pygame.display.flip()
    time.sleep(3)

    # Muestra la pantalla de fin de juego
    if player == player1:
        game.win_game(game_winner, 1)
    else:
        game.win_game(game_winner, 2)


# Funcion principal del programa
if __name__ == "__main__":
    # Inicializa pygame
    pygame.init()

    # Bloquea los eventos del mouse, ya que no se usan
    pygame.event.set_blocked(pygame.MOUSEWHEEL)
    pygame.event.set_blocked(pygame.MOUSEMOTION)
    pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
    pygame.event.set_blocked(pygame.MOUSEBUTTONUP)

    # Ponemos el titulo de la ventana
    pygame.display.set_caption("Teyeliz")

    # Ponemos el icono de la ventana
    icon = pygame.image.load("resources/graphics/icons/iconMetl.png")
    pygame.display.set_icon(icon)

    # Crea la ventana
    WINDOW_SIZE = (760, 412) # Half is 380, 206
    WIDTH, HEIGHT = WINDOW_SIZE
    window = pygame.display.set_mode(WINDOW_SIZE)

    # Carga la fuente
    font = pygame.font.Font("resources/fonts/PressStart2PRegular.ttf", 8)

    # Empaqueta los datos de pygame en una lista
    pygame_data = [pygame.display, window, font]

    # Muestra el menu y obtiene los datos del jugador y el tipo de socket
    menu = Menu(pygame_data)
    player1, player2, socket_type = menu.show_menu()

    # Crea el juego
    game = Game(player1, player2, pygame_data)

    # Inicia el juego, dependiendo del tipo de socket que se haya elegido
    if socket_type == 0: # Servidor
        # Crea el servidor y lo inicia
        server = Server(pygame_data)
        server.start_server()

        # Llama a la funcion que ejecuta el juego, como servidor
        play_game(player1, server.send_data, server.receive_data) # Player1 is server

        # Cierra el servidor
        server.close_server()

    else: # Cliente
        # Crea el cliente y se conecta al servidor
        client = Client(pygame_data)
        client.connect_to_server()

        # Llama a la funcion que ejecuta el juego, como cliente
        play_game(player2, client.send_data, client.receive_data) # Player2 is client
        
        # Cierra el cliente
        client.close_client()

    # Espera a que el usuario presione [CUALQUIER TECLA] para salir
    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                game.quit_game()
            elif event.type == pygame.QUIT:
                game.quit_game()