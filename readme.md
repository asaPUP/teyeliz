# Teyeliz

Teyeliz is a multiplayer card game built with Python and PyGame. It offers an engaging gaming experience where players can compete against each other via WebSockets, using a combination of strategy and luck.

## Overview:

Teyeliz is a turn-based card game where two players, a server and a client, compete against each other. The game involves playing cards strategically to fill a grid and achieve victory conditions. The server manages the game state, while the client interacts with the player through a graphical user interface (GUI) built with PyGame.

## Gameplay:

1. Each player starts with a hand of cards, each representing a combination of different elements, levels and colors, and players take turns playing cards on a desk.
2. The winner of each round places their card on their tic-tac-toe grid, aiming to create lines (rows or columns) of their chosen element-color combinations.
3. The game ends when a player successfully fills a line with their winner cards. Payers must strategize to block their opponent's moves while creating opportunities for their own victories.

## Nahuatl-Inspired Cards:

In Teyeliz, the cards draw inspiration from **elements** of the Nahuatl culture, reflecting the rich heritage of Mesoamerican civilizations. Here are the types of cards in the game and how they interact in-game:

1. **Tletl (Fire)**: "Tletl" cards represent the element of fire and have an advantage over "Metl" (Earth) cards, but are weak against "Atl" (Water) cards.
2. **Metl (Earth)**: "Metl" cards symbolize the stability and resilience of the earth and have an advantage over "Atl" (Water) cards, but are susceptible to "Tletl" (Fire) cards.
3. **Atl (Water)**: "Atl" cards embody the essence of water and are strong against "Tletl" (Fire) cards, but are vulnerable to "Metl" (Earth) cards.

Each card also has a **level** ranging from **1 to 4**, indicating its power within its respective element. Thus, higher-level cards have stronger abilities and can overpower lower-level cards of the same element.

Additionally, **colors** such as **Pink**, **Turquoise**, and **Gold** serve to differentiate one card from another on the grid. These colors do not affect the abilities of the cards, but provide visual distinction and rarity indicators based on the card level.

## Technologies Used:

- **Python 3.11**
- **PyGame** (Python Game Development Library)
- **Socket Programming** (for networking)
- **Pickle** (for data serialization)
- **Git** (Version Control)
- **Linux** (Operating System)

## Installation:

To set up Teyeliz, follow these steps:

1. **Clone** the repository to your local machine.
2. Navigate to the **project directory**.
3. **Create a virtual environment** within the project directory:
   ```bash
   $ python3 -m venv venv
   ```
4. **Activate** the virtual environment:
   ```bash
   $ source ./venv/bin/activate
   ```
5. Install the **required dependencies** using pip:
   ```bash
   $ python3 -m pip install -r requirements.txt
   ```
6. **Run** the main game file script using:
   ```bash
   $ python3 teyeliz.py
   ```
7. When you're finished playing Teyeliz, **deactivate** the virtual environment:
   ```bash
   $ deactivate
   ```
   This ensures that the project's dependencies are installed in an isolated environment, preventing conflicts with other Python projects on your system.

## Usage:

To play Teyeliz, follow these steps:

1. Launch the server by running `python3 teyeliz.py` and selecting option [1] to specify the server mode.
2. Launch the client by running `python3 teyeliz.py` and selecting option [2] to specify the client mode.
3. While in-game, the player can press [SCAPE] or close the window to interrupt their game process and WebSocket connection.
4. When the game ends, each user is prompted to press any key to close their window.

## Contributions:

Contributions to Teyeliz are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -am 'Add some amazing feature'`).
4. Push your branch to your fork (`git push origin feature/AmazingFeature`).
5. Open a pull request.
