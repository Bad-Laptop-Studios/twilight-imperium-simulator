
# Basic Tile
# Basic ship
# System activation
# planet


from map_old import *
from typing import *
from components.units import *
from players import *
from constants import *

class Game():
    def __init__(self, players: int, map_string):
        self.players = []
        for i in range(players):
            self.players.append(Player(i))
        
        self.map = Map()
        self.map.generate_map(map_string)
        self.active_player = None
        
    def start_game(self):
        while True:
            raise NotImplementedError

    def action_phase(self):
        # Add player order
        # Add checking for anomalies

        # Add turn switching
        self.active_player = self.players[0]

        
        print("1: Tactical Action")
        print("2: Strategic Action")
        print("3: Component Action")
        action = int(input("Choose Action: "))
        
        if (action == 1):
            print("Activation")
            self.map.print_map(WIDTH, HEIGHT)
            # Systems will have a number and you enter that number to select it
            system_id = int(input("Choose a system to activate: "))
            active_system = self.activate_system(self.active_player, system_id)
            print("Movement")
            # Choose starting system and system by system move

            
            # Add ability to break loop
            while True:
                route = input("Input a series of systems to travel through: ")
                route = route.split(' ')
 
                # Check if route ends in the active system
                if int(route[-1]) != active_system.get_id():
                    print("Your route must end in the active system.\n Please try again.")
                    continue

                # Check if start of route has a command token from the active player
                if self.system_active(self.active_player, int(route[0])):
                    print("You cannot move units out of a system that contains one of your command tokens.\n Please try again.")

                # Check if all systems in route are adjacent
                cancel = False
                for i in range(len(route)-1):
                    if not self.map.is_adjacent(int(route[i]), int(route[i+1])):
                        print(f"System {route[i]} is not adjacent to System {route[i+1]}.\n Please try again.")
                        cancel = True
                if cancel:
                    continue

                # loop that prints a list of units inside system
                initial_system = self.find_system(int(route[0]))
                units = initial_system.get_units()
                char_to_unit = {}
                for unit in units:
                    # repr should be replaced by a dedicated method displaying unit info
                    print(unit.char() + ': ' + repr(unit) + 'x' + str(units[unit]))
                    char_to_unit[unit.char()] = unit

                
                
                

                # prompts user to select which units they want to move out of the
                # system,check if ship has enough movement to reach the active
                # system
                unit_selection = {}

                # Format e.g c7 C2 W1
                print("Please enter the character of a unit and the number you would like to move from the system in a single line seperated by spaces.")
                selection_input = input('Units to move: ')
                selection_input = selection_input.split(' ')
                # add input error detection
                #convert string input inot dictionary of units
                for selection in selection_input:
                    unit_type = char_to_unit[selection[0]]
                    number = 0
                    if int(selection[1:]) > units[unit_type]:
                        number = units[unit_type]
                    else:
                        number = int(selection[1:])

                    # Check if all units have required movement
                    stats = unit_type.get_stats()
                    if stats[2] < len(route)-1:
                        print(f"Selection: {selection} does not have high enough movement (has {stats[2]} needs {len(route)}). Thus they will be excluded from the movement.")
                        continue

                    unit_selection[unit_type] = number

               
                        
             


                # Add picking up ground forces
                # Add support for sustained units

                # This is from when units were stored as a list
##                print("Enter each ship individually. Enter 'end' to end selection")
##                while selection_input != 'end':
##                    selection_input = int(input("Enter the ship you want to move: "))
##                    stats = units[selection_input].get_stats
##                    
##                    # Check if all ships have high enough movement to travel route
##                    if stats[2] < len(route):
##                        print("The ship must have high enough movement to traverse the route.\n Please try again.")
##                        continue
##                    
##                    unit_selection.append(selection_input)

                

                # Check if any systems have enemy players in them
                cancel = False
                for system_id in route:
                    system_id = int(system_id)
                    if not self.system_safe(self.active_player, system_id):
                        cancel = True
                        print(f"The system at {system_id} contains enemy units, so you cannot move through it.\n Please try again.")

                if cancel:
                    continue

                # Perform movement
                for unit_type in unit_selection:
                    # Move units from initial system to final
                    active_system.add_unit(unit_type, unit_selection[unit_type])
                    initial_system.remove_unit(unit_type, unit_selection[unit_type])

                print("Movement complete")
                self.map.print_map(WIDTH, HEIGHT)

                
                    


        elif action == 2:
            pass
        
        elif action == 3:
            pass

    def find_system(self, system_id: int) -> System:
        systems = self.map.get_systems()
        target_system = systems[system_id]
        return target_system

    def system_safe(self, player: Player, system_id: int) -> bool:
        """
        Returns true if the system has no units or if all units belong to player
        """
        systems = self.map.get_systems()
        target_system = systems[system_id]
        player_id = player.get_id()
        
        units = target_system.get_units()
        for unit in units:
            if unit.get_player_id() != player_id:
                return False
            
        return True
        
        

    def system_active(self, player: Player, system_id: int) -> bool:
        """
        Returns if the player has activated the system
        """
        target_system = self.find_system(system_id)

        if player.get_id() in target_system.activated_by():
            return True

        return False
        
    def activate_system(self,player: Player, system_id: int) -> System:
        """
        Activate the selected system, removing 1 token from the players
        tactic pool. Cannot active a system that already contains one
        of the players command token.
        """
        active_system = self.find_system(system_id)
        # Check if activate player has tactic command tokens
        if player.get_command_tokens('tactic') > 0:
            # Check if system is not activated by player
            if player.get_id() not in active_system.activated_by():     
                # If both true, remove one token from players command pool
                # and activate the system, linking it to the player object
                player.alter_command_tokens("tactic", -1)
                active_system.activate(player.get_id())
                return active_system
                

game = Game(1, "37 71 42 64 24 59 39 75 60 31 29 26 61 79 46 38 78 67 35 28 62 77 45 34 36 27 70 68 73 72 30 47 74 65 76 49 0 20 32 0 44 40 0 43 66 0 22 50 0 33 23 0 63 80 0 25 48 0 21 19")
game.action_phase()
        
    
