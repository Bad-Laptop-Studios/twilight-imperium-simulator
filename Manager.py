# Basic Tile
# Basic ship
# System activation
# planet

from typing import *
class Player:
    """
    Stores token pools, units, owned planets
    """
    def __init__(self):
        self.strategy_card = 0
        self.faction = 0
        self.fleet_token = 0
        self.tactic_token = 0
        self.strategy_token = 0
        
        self.planets = []
        self.ships = []

        self.activated_systems = []

    def select_strategy_card(self, card_number):
        self.strategy_card = card_number

    


class Unit:
    def __init__(self):
        self.cost = 0
        self.combat = 0
        self.combat_multiplier = 1
        self.move = 0
        self.capacity = 0
        self.type = ""
        self.carrying = []

class Structure(Unit):
    def hello(self):
        pass

class Ground_Force(Unit):
    pass
        
class Game():
    def __init__(self):
        self.players = []

    def action_phase(self):
        print("1: Tactical Action")
        print("2: Strategic Action")
        print("3: Component Action")
        action = int(input"Choose Action: "))
        
        if (action == 1):
            print("Activation")
            input("Choose a system to activate: ")
            activate_system()
            active_system = 0
            print("Movement")
            # Choose starting system and system by system move
            
            input("Choose a system to move ships from")

            
            # check if system has a command token from the active player
            # loop that prints a list of units inside system and
            # prompts user to select which units they want to move out of the
            # system,check if ship has enough movement to reach the active
            # system, or don't and tell them when the action fails
            
            # prompt user to choose a adjacent system to move them to
            # check if system

        elif action == 2:
            pass
        
        elif action == 3:
            pass
        
    def activate_system(self):
        """Activate the selected system, removing 1 token from the players
            command pool. Cannot active a system that already contains one
            of the players command token.
        """
        # Check if activate player has command tokens
        # Check if system is not activated by player
        # If both true, remove one token from players command pool
        # and activate the system, linking it to the player object
        pass

    def 
