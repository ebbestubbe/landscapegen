from landscapegen.wavefunction import Wavefunction


def test_collapsed_1():
    wavefunction = [
        [["Grass"]],
    ]
    wf = Wavefunction(wf=wavefunction)
    collapsed = wf.collapsed
    expected = True
    assert collapsed == expected


def test_collapsed_2():
    wavefunction = [
        [["Grass"], ["Grass"], ["Grass"], ["Grass"], ["Grass"]],
        [["Sand"], ["Water"], ["Grass"], ["Grass"], ["Grass"]],
        [["Sand"], ["Sand"], ["Grass"], ["Grass"], ["Grass"]],
        [["Grass"], ["Grass"], ["Grass"], ["Grass"], ["Grass"]],
        [["Sand"], ["Water"], ["Grass"], ["Grass"], ["Grass"]],
    ]
    wf = Wavefunction(wavefunction)
    collapsed = wf.collapsed
    expected = True
    assert collapsed == expected


def test_collapsed_3():
    wavefunction = [
        [["Grass", "Water"], ["Grass"], ["Grass"], ["Grass"], ["Grass"]],
        [["Sand"], ["Water"], ["Grass"], ["Grass"], ["Grass"]],
        [["Sand"], ["Sand"], ["Grass"], ["Grass"], ["Grass"]],
        [["Grass"], ["Grass"], ["Grass"], ["Grass"], ["Grass"]],
        [["Sand"], ["Water"], ["Grass"], ["Grass"], ["Grass"]],
    ]
    wf = Wavefunction(wf=wavefunction)
    collapsed = wf.collapsed
    expected = False
    assert collapsed == expected


def test_collapsed_4():
    wavefunction = [
        [["Grass"], ["Grass"], ["Grass"], ["Grass"], ["Grass"]],
        [["Sand"], ["Water"], ["Grass"], ["Grass"], ["Grass"]],
        [["Sand"], ["Sand"], ["Grass"], ["Grass"], ["Grass"]],
        [["Grass"], ["Grass"], ["Grass", "Water", "Lava"], ["Grass"], ["Grass"]],
        [["Sand"], ["Water"], ["Grass"], ["Grass"], ["Grass"]],
    ]
    wf = Wavefunction(wf=wavefunction)
    collapsed = wf.collapsed
    expected = False
    assert collapsed == expected
