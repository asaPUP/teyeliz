"""
Teyeliz - A card game for two players with TCP websockets and pygame
"""

# Import Python modules
import pygame
from pygame.locals import *
import time

# Import game modules
from data.menu import Menu
from data.game import Game
from data.server import Server
from data.client import Client

# Function to execute the game
def play_game(player, send_data_func, receive_data_func):
    # Main game loop
    while True:
        # Handle keyboard events
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

        # Player selects a card and plays it
        game.show_hud(player)  # Show player's HUD
        card_index1, played_data1 = game.select_card(player)

        # Send data to the opponent
        send_data_func(card_index1, played_data1)

        # Receive data from the opponent
        card_index2, played_data2 = receive_data_func()

        # Determine which player wins the round
        if player == player1:  # If the player is the server (player1)
            round_winner = game.compare_cards(played_data1, played_data2)
        else:  # If the player is the client (player2)
            round_winner = game.compare_cards(played_data2, played_data1)

        # Show the round result
        game.win_round(round_winner)

        # Check if there's a game winner and if so, end the game
        game_winner = game.check_winner()
        if game_winner > 0:
            break

        # Start a new round
        if player == player1:  # If player is the server (player1)
            game.new_round(card_index1, card_index2)
        else:  # If player is the client (player2)
            game.new_round(card_index2, card_index1)

    # Draw a white box around the winner's grid
    if game_winner == 1:
        pygame.draw.rect(window, (255, 255, 255), (62, 62, 154, 154), 5)
        pygame.display.flip()
    else:
        pygame.draw.rect(window, (255, 255, 255), (544, 62, 154, 154), 5)
        pygame.display.flip()
    time.sleep(3)

    # Show the end game screen
    if player == player1:
        game.win_game(game_winner, 1)
    else:
        game.win_game(game_winner, 2)


# Main function of the program
if __name__ == "__main__":
    # Initialize pygame
    pygame.init()

    # Block mouse events as they are not used
    pygame.event.set_blocked(pygame.MOUSEWHEEL)
    pygame.event.set_blocked(pygame.MOUSEMOTION)
    pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
    pygame.event.set_blocked(pygame.MOUSEBUTTONUP)

    # Set window title
    pygame.display.set_caption("Teyeliz")

    # Set window icon
    icon = pygame.image.load("resources/graphics/icons/iconMetl.png")
    pygame.display.set_icon(icon)

    # Create the window
    WINDOW_SIZE = (760, 412)  # Half is 380, 206
    WIDTH, HEIGHT = WINDOW_SIZE
    window = pygame.display.set_mode(WINDOW_SIZE)

    # Load font
    font = pygame.font.Font("resources/fonts/PressStart2PRegular.ttf", 8)

    # Pack pygame data into a list
    pygame_data = [pygame.display, window, font]

    # Show the menu and get player data and socket type
    menu = Menu(pygame_data)
    player1, player2, socket_type = menu.show_menu()

    # Create the game
    game = Game(player1, player2, pygame_data)

    # Start the game, depending on the chosen socket type
    if socket_type == 0:  # Server
        # Create and start the server
        server = Server(pygame_data)
        server.start_server()

        # Call the function that executes the game as the server
        play_game(player1, server.send_data, server.receive_data)  # Player1 is server

        # Close the server
        server.close_server()

    else:  # Client
        # Create the client and connect to the server
        client = Client(pygame_data)
        client.connect_to_server()

        # Call the function that executes the game as the client
        play_game(player2, client.send_data, client.receive_data)  # Player2 is client

        # Close the client
        client.close_client()

    # Wait for the user to press any key to exit
    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                game.quit_game()
            elif event.type == pygame.QUIT:
                game.quit_game()
