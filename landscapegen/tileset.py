class Tileset_wfc:
    # Only to be used with wave function collapse
    def __init__(self, info, connections) -> None:
        self.info = info
        self.connections = connections
        self.characters = list(info.keys())

    # Do we want to later include special "allowed/not allowed" categories?
    # def __init__(self, info, connections, allowed= None) -> None:
    #     self.info = info
    #     self.connections=connections
    #     # In case there are special rules where not all tiles in the tileset are
    #     # allowed.
    #     if allowed is None:
    #         self.allowed = info.keys()
    #     else:
    #         self.allowed = allowed
