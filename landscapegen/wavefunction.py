class Wavefunction:
    def __init__(self, wf):
        # wf is a triple array where the first 2 dimensions are rectangular, and
        # the contents are arrays of strings,  eg:
        # wf = [
        #     [["Grass"], ["Grass", "Lava"]],
        #     [["Sand"], ["Water"]],
        #     [["Sand"], ["Sand", "Grass"]],
        # ]
        self.wf = wf
        self.size0 = len(wf)
        self.size1 = len(wf[0])

    @property
    def collapsed(self):
        # Go through all points and figure out of there are more than 1 element in each.
        for i, row in enumerate(self.wf):
            for j, col in enumerate(row):
                if len(col) > 1:
                    return False
        return True
