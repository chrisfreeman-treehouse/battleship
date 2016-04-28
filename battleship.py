#!/usr/bin/python3
"""Implements the classic Battleship board game.

Project 2 - Treehouse Techdegree - Python Web Development
"""
from constants import SHIP_INFO
from models import Player, Ship
from utils import (clear_screen, is_legal_coord, print_legend, show_banner)

__author__ = "Chris Freeman"
__copyright__ = "Copyright 2016, Chris Freeman"
__license__ = "MIT"

# ignore pylint warning about using 'input'
# pylint: disable=bad-builtin


def ask_player_name(moniker="player"):
    """Ask for player's name"""
    name = None
    # get player name
    while not name:
        name = input("Enter the name of {}: ".format(moniker)).strip()
        if not name:
            print("Empty name not allowed")
    print("Thanks {}!".format(name))
    return name


def print_board(player_name, player_view):
    """Print a player board

    Args:
        player_name (str): name of current player
        player_view (List[str]): list of strings representing board view
    """

    # board titles
    print("   {:_^22}\n".format(player_name + "'s board:"))
    # stitch together board views for display
    for player_line in player_view:
        print("   {:22}".format(player_line))
    print_legend()


def print_all_boards(opp_name, player_name, opp_view, player_view):
    """Print both player boards

    Args:
        opp_name (str): name of opponent
        player_name (str): name of current player
        opp_view (List[str]): list of strings representing board view
        player_view (List[str]): list of strings representing board view
    """

    # boards titles
    print("   {:_^22}        {:_^22}\n".format(
        opp_name + "'s board:", player_name + "'s board:"))
    # stitch together board views for display
    for opp_line, player_line in zip(opp_view, player_view):
        print("   {:22}        {:22}".format(opp_line, player_line))
    print_legend()


def gen_ship_coords(anchor, size, direction):
    """Generate ship board coordinate based on anchor location and size

    The ship coordinates start at the anchor position and run Down for
    vertical direction and run Right for horizontal direction.

    Verify ship fits on board.

    Args:
        anchor (str): two character board coordinate "A1"
        size (int): size of ship in board spaces
        orientation (str): is ship Horizontal or Vertical

    Returns:
        List[str]: list of board coordinates, if valid. Empty list otherwise.
    """
    ship_col = ord(anchor[0].upper())
    ship_row = int(anchor[1:])
    if direction[0].lower() == 'v':
        # ship runs vertically DOWN from anchor
        coords = [chr(ship_col) + str(row)
                  for row in range(ship_row, ship_row + size)]
    else:
        # ship runs horizontally RIGHT from anchor
        coords = [chr(col) + str(ship_row)
                  for col in range(ship_col, ship_col + size)]
    # check if ship bow and stern are on board
    if is_legal_coord(coords[0]) and is_legal_coord(coords[-1]):
        # coords confirmed
        return coords
    else:
        # bad ship coords
        print("Error: not all coords on board: ", coords)
        return []


def get_anchor_coord():
    """Ask user for ship anchor coordinates"""
    while True:
        response = input("What is the upper-most or left-most ship postion "
                         "(for example D4): ").strip()
        anchor = response.upper()
        if is_legal_coord(anchor):
            return anchor
        else:
            print("Coordnate {} is not on the board. Please enter Letter "
                  "and Number as one word.".format(response))


def get_guess(player):
    """Ask user for guess"""
    while True:
        response = input("Enter {}'s guess (for example D4): "
                         "".format(player.name)).strip()
        guess = response.upper()
        if guess in player.guesses:
            print("Coordnate {} already guessed. Try Again."
                  "".format(response))
            continue
        if is_legal_coord(guess):
            return guess
        else:
            print("Coordnate {} is not on the board. Please enter Letter "
                  "and Number as one word.".format(response))


def get_vert_or_horiz():
    """Ask user for vertical or horizontal direction"""
    while True:
        response = input(
            "Does this ship run [V]ertical, or [H]orizontal: ").strip()
        if not response:
            print("Error: Blank not allowed. Please Enter 'v' or 'h'!")
            continue
        direction = response[0].lower()
        if direction == 'v' or direction == 'h':
            return direction
        else:
            print("Error: Response {} not valid. Please Enter 'v' or 'h'!"
                  "".format(response))


def define_fleet(player):
    """Define player's ships and place on board"""
    # place each ship
    for ship_spec in SHIP_INFO:
        ship_name = ship_spec[0]
        ship_size = ship_spec[1]
        # display top banner
        clear_screen()
        show_banner()
        print("Placing Ships for {}:\n".format(player.name))
        # display board
        print_board(player.name, player.board.get_player_view())
        # display ship info
        print("Placing {} (size:{})\n".format(ship_name, ship_size))

        # get ship placement details
        while True:
            # 1. ask if vertical or horizontal
            direction = get_vert_or_horiz()
            # 2. ask for top or left starting coordinate
            anchor = get_anchor_coord()
            # 3. validate input (explain why input rejected)
            coords = gen_ship_coords(anchor, ship_size, direction)
            # 4. validate ship placement
            if not coords:
                print("Error: ship coordinates not all on the board\n")
                continue
            if not player.board.verify_empty(coords):
                print("Error: ship coordinates collide with other ships. "
                      "Try again\n")
                continue
            # input valid; last while loop
            break
        # create ship from input
        ship = Ship(ship_name, ship_size, coords, direction)
        # add ship to players list
        player.add_ship(ship)
        # place ship on game board
        player.board.place_ship(ship)
        # 5. redraw screen for next ship (at top of loop)
    # display top banner
    clear_screen()
    show_banner()
    # display board
    print("Placing Ships for {}:\n".format(player.name))
    print_board(player.name, player.board.get_player_view())
    input("All ships placed for {}. Hit ENTER to continue...."
          "".format(player.name))
    clear_screen()


def take_turn(player, opponent):
    """Take a turn"""

    clear_screen()
    show_banner()
    input("It's {}'s turn. Hit ENTER to continue....".format(player.name))

    clear_screen()
    show_banner()
    print("It's {}'s turn:\n".format(player.name))
    # print boards for guessing
    opp_view = opponent.board.get_opponent_view()
    player_view = player.board.get_player_view()

    # stitch together board views for display
    print_all_boards(opponent.name, player.name, opp_view, player_view)

    coord = get_guess(player)
    # remember guessed coordinates
    player.guesses.append(coord)
    # process guess
    response = opponent.board.guess(coord)

    # update board and display response
    opp_view = opponent.board.get_opponent_view()

    # reprint boards
    clear_screen()
    show_banner()
    print("It's {}'s turn:\n".format(player.name))
    # print both boards
    print_all_boards(opponent.name, player.name, opp_view, player_view)
    print(response)

    input("Hit ENTER to clear screen and end your turn....")
    clear_screen()


def main():
    """Run the console-based python game"""
    # start with a clear screen
    clear_screen()
    show_banner()
    # ask for players names
    name1 = ask_player_name("Player 1")
    name2 = ask_player_name("Player 2")
    # initiate player instances
    player1 = Player(name1)
    player2 = Player(name2)
    input("\nNext you'll each add your ships. {} first. (No peeking {})\n\n"
          "Hit ENTER to continue....".format(name1, name2))

    # placing ships
    clear_screen()
    # defind player1's fleet and add to board
    define_fleet(player1)
    show_banner()
    input("Time to add {}'s ships. Hit ENTER to continue....".format(name2))
    # define player2's fleet and add to board
    define_fleet(player2)

    # commense game play
    show_banner()
    input("Game Time! {} goes first. Hit ENTER to continue....".format(name1))
    game_continue = True
    while game_continue:
        take_turn(player1, player2)
        if not player2.ships_left():
            show_banner()
            input("{} WINS!!! Hit ENTER to see final boards....\n"
                  "".format(player1.name))
            game_continue = False
            continue
        take_turn(player2, player1)
        if not player1.ships_left():
            show_banner()
            input("{} WINS!!! Hit ENTER to see final boards....\n"
                  "".format(player2.name))
            game_continue = False

    # Display final boards
    print_all_boards(player1.name, player2.name,
                     player1.board.get_player_view(),
                     player2.board.get_player_view())


if __name__ == '__main__':
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\n quitting....")
