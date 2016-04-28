#!/usr/bin/python3
"""Utility functions used across Battleship projeect.

Project 2 - Treehouse Techdegree - Python Web Development
"""
from constants import (BANNER, BOARD_SIZE, VERTICAL_SHIP,
                       HORIZONTAL_SHIP, EMPTY, MISS, HIT, SUNK)

__author__ = "Chris Freeman"
__copyright__ = "Copyright 2016, Chris Freeman"
__license__ = "MIT"


def clear_screen():
    """Clear screen using VT Esc sequence"""
    print("\033c", end="")


def show_banner():
    """print game banner"""
    print(BANNER)


def print_legend():
    """Print legend of board symbols"""
    print("Legend: Ships {} or {}   Empty {}   Miss {}   Hit {}   Sunk {}\n"
          "".format(VERTICAL_SHIP, HORIZONTAL_SHIP, EMPTY, MISS, HIT, SUNK))


def offset_to_coord(row, col):
    """Generate board coordinates from a row and column number

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
