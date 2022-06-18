from constants import *

class LawSet():
    """ Collection of all the laws in the game. Contains initial state of all laws. """
    def __init__(self) -> None:
        self._maximum_action_cards = 7
        self._maximum_command_tokens = 16
        self._maximum_victory_points = 10   # yes I put it here, get over it haha

class Table():
    """ The primary View class. Stores the state of the entires table. """
    def __init__(self):
        laws = LawSet()