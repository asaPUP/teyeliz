# Import Python modules
import pygame
from pygame.locals import *
import time

# Import custom modules
from data.menu import Menu
from data.game import Game
from data.server import Server
from data.client import Client

# Play game function
def play_game(player, send_data_func, receive_data_func):
    # Game loop
    while True:
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

        # Player plays a card
        game.show_hud(player) # Show HUD of the player
        card_index1, played_data1 = game.select_card(player)

        # Send data to the opponent
        send_data_func(card_index1, played_data1)

        # Receive data from the opponent
        card_index2, played_data2 = receive_data_func()

        # Check who wins the round, return the winner
        if player == player1: # If player is server (player1)
            round_winner = game.compare_cards(played_data1, played_data2)
        else: # If player is client (player2)
            round_winner = game.compare_cards(played_data2, played_data1)

        # Show who wins the round
        game.win_round(round_winner)

        # Check if there is a game winner, return the winner or 0 if there is no winner
        game_winner = game.check_winner()

        # If there is a game winner, show the winner and return the winner
        if game_winner > 0:
            break

        # Create a new round, draw new cards and increase the round number
        if player == player1: # If player is server (player1)
            game.new_round(card_index1, card_index2)
        else: # If player is client (player2)
            game.new_round(card_index2, card_index1)

    # When the game is over, show the screen still for 2 seconds
    # Encierra el tic tac toe del ganador en un rectangulo transparente de borde blanco
    if game_winner == 1:
        # El cuadrado va de (62, 62) a (216, 216)
        pygame.draw.rect(window, (255, 255, 255), (62, 62, 154, 154), 5)
        pygame.display.flip()
    else:
        # El cuadrado va de (544, 62) a (698, 216)
        pygame.draw.rect(window, (255, 255, 255), (544, 62, 154, 154), 5)
        pygame.display.flip()
    time.sleep(3)

    # Show the winner screen
    if player == player1:
        game.win_game(game_winner, 1)
    else:
        game.win_game(game_winner, 2)


# Main function
if __name__ == "__main__":
    # Initialize pygame
    pygame.init()

    # Set window title
    pygame.display.set_caption("Teyeliz")

    # create window
    WINDOW_SIZE = (760, 412) # Half is 380, 206
    WIDTH, HEIGHT = WINDOW_SIZE
    window = pygame.display.set_mode(WINDOW_SIZE)

    # Load font
    font = pygame.font.Font("resources/fonts/PressStart2PRegular.ttf", 8)

    pygame_data = [pygame.display, window, font]

    # Create and show menu
    menu = Menu(pygame_data)
    player1, player2, socket_type = menu.show_menu() # Shows menu and returns player1, player2, and socket_type

    # Create game
    game = Game(player1, player2, pygame_data)

    # Start the game depending on the socket type (server or client)
    if socket_type == 0: # Server
        # Create the server and start it
        server = Server(pygame_data)
        server.start_server()

        # Start the game
        play_game(player1, server.send_data, server.receive_data) # Player1 is server

        # Close the server
        server.close_server()

    else: # Client
        # Create the client and connect to the server
        client = Client(pygame_data)
        client.connect_to_server()

        # Start the game
        play_game(player2, client.send_data, client.receive_data) # Player2 is client
        
        # Close the client
        client.close_client()

    # Wait for the user to press ANY KEY to exit or R to restart
    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                game.quit_game()
            elif event.type == pygame.QUIT:
                game.quit_game()