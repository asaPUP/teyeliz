# Import Python modules
import socket
import pickle

# Import custom modules
from data.menu import Menu
from data.game import Game
from data.server import Server
from data.client import Client

# Test code
if __name__ == "__main__":
    # Create menu
    menu = Menu()

    # Show menu
    player1, player2, socket_type = menu.show_menu()

    # Create game
    game = Game(player1, player2)

    if socket_type == 0:  # Server
        server = Server()

        # Start the server
        server.start_server()

        while True:
            # P1 plays a card
            game.show_hud(player1)
            card_index1, played_data1 = game.select_card(player1)

            # Send data to the client
            server.send_data(card_index1, played_data1)

            # Receive data from the client
            card_index2, played_data2 = server.receive_data()

            # Check who wins the round
            round_winner = game.compare_cards(played_data1, played_data2)

            # Show who wins the round
            game.win_round(round_winner)

            # Check if there is a game winner
            game_winner = game.check_winner()

            if game_winner > 0:
                game.win_game(game_winner)
                break

            # Create new round
            game.new_round(card_index1, card_index2)

        server.close_server()

    elif socket_type == 1:  # Client
        client = Client()

        # Connect to the server
        client.connect_to_server()

        while True:
            # P2 plays a card
            game.show_hud(player2)
            card_index2, played_data2 = game.select_card(player2)

            # Send data to the server
            client.send_data(card_index2, played_data2)

            # Receive data from the server
            card_index1, played_data1 = client.receive_data()

            # Check who wins the round
            round_winner = game.compare_cards(played_data1, played_data2)

            # Show who wins the round
            game.win_round(round_winner)

            # Check if there is a game winner
            game_winner = game.check_winner()

            if game_winner > 0:
                game.win_game(game_winner)
                break

            # Create new round
            game.new_round(card_index1, card_index2)

        client.close_client()