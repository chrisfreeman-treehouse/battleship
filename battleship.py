#!/usr/bin/python3
"""Battleship - Treehouse Techdegree - Python Web Development

Implements the classic board game Battleship.
"""
__author__ = "Chris Freeman"
__copyright__ = "Copyright 2016, Chris Freeman"
__license__ = "MIT"

# ignore pylint warning about using 'input'
# pylint: disable=bad-builtin

SHIP_INFO = [
    # ("Aircraft Carrier", 5),
    # ("Battleship", 4),
    # ("Submarine", 3),
    # ("Cruiser", 3),
    ("Patrol Boat", 2)
]

BOARD_SIZE = 10

VERTICAL_SHIP = '|'
# Using mdash instead of hyphen
HORIZONTAL_SHIP = '\u2014'
EMPTY = 'O'
MISS = '.'
HIT = '*'
SUNK = '#'

BANNER = r"""
 ____        _   _   _           _     _
| __ )  __ _| |_| |_| | ___  ___| |__ (_)_ __
|  _ \ / _` | __| __| |/ _ \/ __| '_ \| | '_ \
| |_) | (_| | |_| |_| |  __/\__ \ | | | | |_) |
|____/ \__,_|\__|\__|_|\___||___/_| |_|_| .__/
                                        |_|
"""


def clear_screen():
    """Clear screen using VT Esc sequence"""
    print("\033c", end="")


def show_banner():
    """print game banner"""
    print(BANNER)


def print_legend():
    """Print legend of board symbols"""
    print("Legend: Ships {} or {}, Empty:{}, Miss:{}, Hit:{}, Sunk:{}\n"
          "".format(VERTICAL_SHIP, HORIZONTAL_SHIP, EMPTY, MISS, HIT, SUNK))


def ask_player_name(moniker="player"):
    """Prompted for both players' names"""
    name = None
    # get player name
    while not name:
        name = input("Enter the name of {}: ".format(moniker)).strip()
        if not name:
            print("Empty name not allowed")
    print("Thanks {}!".format(name))
    return name


def board_heading():
    """Return board heading string"""
    return ("   " + " ".join(
        [chr(c) for c in range(ord('A'), ord('A') + BOARD_SIZE)]))


def print_boards(opp_name, player_name, opp_view, player_view):
    """Print both player boards"""
    # boards titles
    print("   {:_^22}        {:_^22}\n".format(
        opp_name + "'s board:", player_name + "'s board:"))
    # stitch together board views for display
    for opp_line, player_line in zip(opp_view, player_view):
        print("   {:22}        {:22}".format(opp_line, player_line))


def offset_to_coord(row, col):
    """Generate board coordinate from a row and column number

    Args:
        row (int): row offset
        col (int): column offset

    Returns:
        str: String coordinate in the form "A10"
    """
    return chr(ord('A') + col) + str(row + 1)


def coord_to_offset(coord):
    """Generate a row and column number from a board coordinate

    Args:
        str: String coordinate in the form "A10"

    Returns: tuple (row, column)
        row (int): 0-based row offset
        col (int): 0-based column offset
    """
    col = ord(coord[0]) - ord('A')
    row = int(coord[1:]) - 1
    return (row, col)


def is_legal_coord(coord, board_size=BOARD_SIZE):
    """Verify coordinate is on the game board

    Args:
        coord (str): board coordinate "<letter><number>"
        board_size (int): size of board. Defualt

    Returns:
        bool: True if coordinate is legal and on the board, False otherwise.
    """
    if len(coord) < 2:
        # coord  is too short to be legal
        return False
    # covert or return False
    try:
        ship_col = ord(coord[0].upper())
        ship_row = int(coord[1:])
    except (TypeError, ValueError):
        return False
    # check if coord is on board
    return (ship_col >= ord('A') and ship_col <= ord('A') + board_size - 1 and
            ship_row >= 1 and ship_row <= board_size)


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
        print("\n".join(player.board.get_player_view()))
        # display ship banner
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
    print("\n".join(player.board.get_player_view()))
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
    print_boards(opponent.name, player.name, opp_view, player_view)

    coord = player.get_guess()
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
    print_boards(opponent.name, player.name, opp_view, player_view)
    # print("{}'s board:\n".format(opponent.name))
    # view = opponent.board.get_opponent_view()
    print(response)

    input("Hit ENTER to clear screen and end your turn....")
    clear_screen()


class Ship():
    """Ship with name, size, coordinates, and hits

    Args:
        name (str): Name of the ship
        size (int): ship size (in board squares)
        coords (list[str]): list of ship board coords
        direction (str): ship direction vertical or horizontal

    Attributes:
        hits (int): coords "hit" by guess
        sunk (bool): all coords "hit"
        char (str): display character "|" vertical "-" horizontal
    """

    def __init__(self, name, size, coords, direction):
        """Initialize Ship with name, size and coordinates
        """
        self.name = name
        self.size = size
        self.coords = coords
        self.direction = direction
        # List[str]: coordinates of ship that has been "hit"
        self.hits = []
        # Boolean: Has this ship sunk (all coords "hit")
        self.sunk = False
        # str: display character
        if direction.lower() == 'v':
            self.char = VERTICAL_SHIP
        else:
            self.char = HORIZONTAL_SHIP

    def get_state_player(self, coord):
        """Display SUNK, HIT, or ship charactera"""
        if self.sunk:
            return SUNK
        elif coord in self.hits:
            return HIT
        else:
            return self.char

    def get_state_opponent(self, coord):
        """Display SUNK, HIT, or EMPTY (do not give away position)"""
        if self.sunk:
            return SUNK
        elif coord in self.hits:
            return HIT
        else:
            return EMPTY

    def hit(self, coord):
        """Apply a hit at this coord"""
        if coord.upper() in self.coords:
            # capture Hit!
            self.hits.append(coord)
            # check if sunk
            if len(self.hits) == self.size:
                self.sunk = True
                self.char = SUNK
                return SUNK
            else:
                return HIT


class Player():
    """Player representing name and placed ships

    Args:
        name (str): players name

    Attributes:
        board (Board): players game board
        ships (List[Ship]): list of player ships
        guesses (List[str]): list of coordinates guessed
    """

    def __init__(self, name):
        """Define player's name, board, ships, guesses"""
        self.name = name
        # create dict of player's ships
        self.board = Board()
        self.ships = []
        self.guesses = []
        # for ship_name, ship_size in SHIP_INFO:
        #     self.ships[ship_name] = Ship(ship_name, size)

    def add_ship(self, ship):
        """add ship to current list of ships"""
        self.ships.append(ship)

    def ships_left(self):
        """Search for unsunken ships"""
        found = False
        for ship in self.ships:
            if not ship.sunk:
                found = True
        return found

    def get_guess(self):
        """Ask user for guess"""
        while True:
            response = input("Enter {}'s guess (for example D4): "
                             "".format(self.name)).strip()
            guess = response.upper()
            if guess in self.guesses:
                print("Coordnate {} already guessed. Try Again."
                      "".format(response))
                continue
            if is_legal_coord(guess):
                return guess
            else:
                print("Coordnate {} is not on the board. Please enter Letter "
                      "and Number as one word.".format(response))


class Location():
    """A single board location tracking state and ships

    Args:
        coord (str): coordiante name "A10"

    Attributes:
        ship (Ship): the Ship occupying this location
    """

    def __init__(self, coord):
        "docstring"
        self.coord = coord
        self.ship = None
        self.state = EMPTY

    def player_view(self):
        """print board location as seen by player"""
        if self.ship:
            return self.ship.get_state_player(self.coord)
        else:
            return self.state

    def opponent_view(self):
        """print board location as seen by oppoment"""
        if self.ship:
            return self.ship.get_state_opponent(self.coord)
        else:
            return self.state

    def guess(self):
        """process a guess at this location"""
        if not self.ship:
            # a miss
            self.state = MISS
        else:
            self.state = self.ship.hit(self.coord)
        return self.state


class Board():
    """Battleship Board

    Board is a square array of Locations
    """

    def __init__(self, size=BOARD_SIZE):
        """initialize board to correct size"""
        self.size = size
        self.grid = []
        # Add 'size' number of rows
        for row in range(self.size):
            # Add 'size' number of Locations per row
            new_row = []
            for col in range(self.size):
                new_row.append(Location(offset_to_coord(row, col)))
            self.grid.append(new_row)

    def get_player_view(self):
        """Return player view of game board (with ships revealed)"""
        view = [board_heading()]
        row_num = 1
        for row in self.grid:
            view.append(str(row_num).rjust(2) + " " + " ".join(
                [location.player_view() for location in row]))
            row_num += 1
        view.append("")
        return view

    def get_opponent_view(self):
        """Return opponent view of game board (without revealing ships)"""
        view = [board_heading()]
        row_num = 1
        for row in self.grid:
            view.append(str(row_num).rjust(2) + " " + " ".join(
                [location.opponent_view() for location in row]))
            row_num += 1
        view.append("")
        return view

    def verify_empty(self, coords):
        """Verify all coordinates are clear of ships"""
        result = True
        for coord in coords:
            row, col = coord_to_offset(coord)
            # assign location ship to this ship
            if self.grid[row][col].ship:
                result = False
        return result

    def place_ship(self, ship):
        """Place Ship on board"""
        for coord in ship.coords:
            row, col = coord_to_offset(coord)
            # assign location ship to this ship
            self.grid[row][col].ship = ship

    def guess(self, coord):
        """Apply guess to board"""
        row, col = coord_to_offset(coord)
        result = self.grid[row][col].guess()
        if result == MISS:
            response = "Guess [{}]: You Missed!\n".format(coord)
        elif result == HIT:
            response = "Guess [{}]: You Hit!!\n".format(coord)
        elif result == SUNK:
            response = "Guess [{}]: You SUNK my {}!!!\n".format(
                coord, self.grid[row][col].ship.name)
        return response


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
    print_boards(player1.name, player2.name,
                 player1.board.get_player_view(),
                 player2.board.get_player_view())


if __name__ == '__main__':
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\n quitting....")
