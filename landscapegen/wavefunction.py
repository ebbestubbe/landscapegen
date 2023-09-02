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

    def __eq__(self, other):
        if not isinstance(other, Wavefunction):
            return False
        if (self.size0 != other.size0) or (self.size1 != other.size1):
            return False
        for j in range(self.size0):
            for i in range(self.size1):
                if not set(self.wf[j][i]) == set(other.wf[j][i]):
                    return False
        return True

    @property
    def collapsed(self):
        # Go through all points and figure out of there are more than 1 element
        # in each.
        for i, row in enumerate(self.wf):
            for j, col in enumerate(row):
                if len(col) > 1:
                    return False
        return True

    @property
    def contains_blank(self):
        for i, row in enumerate(self.wf):
            for j, col in enumerate(row):
                if col[0] == "__BLANK__":
                    return True

        return False
