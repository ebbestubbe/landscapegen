class Tileset_wfc:
    # Only to be used with wave function collapse
    def __init__(self, info, connections) -> None:

        self.info = info
        #self.info["__BLANK__"] = [1, 0, 1, 1]
        self.connections = connections
        self.characters = list(self.info.keys())
        self.char_list = list(self.info.keys()) 
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
