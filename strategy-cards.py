class StrategyCard():
    def __init__(self):
        self._name = None
        self._is_exhausted = False

    def resolve_primary(self):
        raise NotImplementedError

    def resolve_secondary(self):
        raise NotImplementedError

class Leadership(StrategyCard):
    def __init__(self):
        pass

    def resolve_primary(self):
        raise NotImplementedError

    def resolve_secondary(self):
        raise NotImplementedError

class Diplomacy(StrategyCard):
    def __init__(self):
        pass

    def resolve_primary(self):
        raise NotImplementedError

    def resolve_secondary(self):
        raise NotImplementedError
    
class Politics(StrategyCard):
    def __init__(self):
        pass

    def resolve_primary(self):
        raise NotImplementedError

    def resolve_secondary(self):
        raise NotImplementedError

class Construction(StrategyCard):
    def __init__(self):
        pass

    def resolve_primary(self):
        raise NotImplementedError

    def resolve_secondary(self):
        raise NotImplementedError
    
class Trade(StrategyCard):
    def __init__(self):
        pass

    def resolve_primary(self):
        raise NotImplementedError

    def resolve_secondary(self):
        raise NotImplementedError
    
class Warfare(StrategyCard):
    def __init__(self):
        pass

    def resolve_primary(self):
        raise NotImplementedError

    def resolve_secondary(self):
        raise NotImplementedError
    
class Technology(StrategyCard):
    def __init__(self):
        pass

    def resolve_primary(self):
        raise NotImplementedError

    def resolve_secondary(self):
        raise NotImplementedError
    
class Imperial(StrategyCard):
    def __init__(self):
        pass

    def resolve_primary(self):
        raise NotImplementedError

    def resolve_secondary(self):
        raise NotImplementedError
    