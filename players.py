class Player:
    """
    Stores token pools, units, owned planets
    """
    def __init__(self, id: int):
        self.strategy_card = 0
        self.faction = 0
        self.fleet_token = 0
        self.tactic_token = 0
        self.strategy_token = 0
        
        self.planets = []
        self.ships = []

        self.activated_systems = []

        self.id = id

    def select_strategy_card(self, card_number):
        self.strategy_card = card_number

    def deactivate_systems(self):
        """
        Remove all activated systems
        """
        self.activated_systems = []

    def get_id(self) -> int:
        return self.id
    
