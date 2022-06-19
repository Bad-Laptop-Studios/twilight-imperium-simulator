import sys
sys.path.append('components/')

# Basic Tile
# Basic ship
# System activation
# planet
import sys
sys.path.append("components/")


from map import *
from typing import *
from units import *
from players import *
from using import *

class Game():
    def __init__(self, players: int, map_string):
        self.players = []
        for i in range(players):
            self.players.append(Player(i+1))
        
        self.map = Map()
        self.map.generate_map(map_string)
        self.active_player = 0
        
    def start_game(self):
        while True:
            raise NotImplementedError

    def action_phase(self):
        # Add player order
        self.active_player = self.players[0]
        print("1: Tactical Action")
        print("2: Strategic Action")
        print("3: Component Action")
        action = int(input("Choose Action: "))
        
        if (action == 1):
            print("Activation")
            self.map.print_map(WIDTH, HEIGHT)
            # Systems will have a number and you enter that number to select it
            system_id = input("Choose a system to activate: ")
            active_system = activate_system()
            print("Movement")
            # Choose starting system and system by system move
            
            position_idinput("Choose a system to move ships from")

            
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
        
    def activate_system(self, active_player: Player, system_id: int) -> System:
        """
        Activate the selected system, removing 1 token from the players
        tactic pool. Cannot active a system that already contains one
        of the players command token.
        """
        # Check if activate player has command tokens
        if active_player.get_fleet_tokens() > 0:
            # Check if system is not activated by player
            if active_player.get_id() not in active_player.activated_by():     
                # If both true, remove one token from players command pool
                # and activate the system, linking it to the player object
                active_player.alter_command_tokens(-1, "tactic")
                systems = self.map.get_systems()
                active_system = systems[system_id]
                active_system.activate(active_player.get_id())
                return active_system
                
        
        
    
