class Tileset_wfc:
    # Only to be used with wave function collapse
    def __init__(self, info, connections) -> None:

        self.info = info
        self.connections = connections
        self.characters = list(self.info.keys())
