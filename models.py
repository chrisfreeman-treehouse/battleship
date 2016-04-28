#!/usr/bin/python3
"""Class definitions used across Battleship projeect.

Project 2 - Treehouse Techdegree - Python Web Development
"""
from constants import (BOARD_HEADING, BOARD_SIZE, VERTICAL_SHIP,
                       HORIZONTAL_SHIP, EMPTY, MISS, HIT, SUNK)
from utils import coord_to_offset, offset_to_coord

__author__ = "Chris Freeman"
__copyright__ = "Copyright 2016, Chris Freeman"
__license__ = "MIT"


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
        view = [BOARD_HEADING]
        row_num = 1
        for row in self.grid:
            view.append(str(row_num).rjust(2) + " " + " ".join(
                [location.player_view() for location in row]))
            row_num += 1
        view.append("")
        return view

    def get_opponent_view(self):
        """Return opponent view of game board (without revealing ships)"""
        view = [BOARD_HEADING]
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
        """Return board location state as seen by player"""
        if self.ship:
            return self.ship.get_state_player(self.coord)
        else:
            return self.state

    def opponent_view(self):
        """Return board location state as seen by oppoment"""
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
