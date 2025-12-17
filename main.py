from landscapegen.factory import coast_boundary_factory
from landscapegen.factory import simple_tileset_factory
from landscapegen.pygqt_plotting import pyqt_plot
from landscapegen.wavefunction import generate_collapsed_wfc
from landscapegen.wavefunction import generate_undertermined_wavefunction
from landscapegen.wavefunction import Wavefunction


def plot_example_pyqt_2():
    height = 10
    width = 15

    tileset = simple_tileset_factory()

    wavefunction = generate_collapsed_wfc(tileset=tileset, height=height, width=width)

    pyqt_plot(wavefunction=wavefunction, tileset=tileset)


def plot_completely_undetermined_coast():
    height = 7
    width = 10
    tileset = coast_boundary_factory()
    wavefunction = generate_undertermined_wavefunction(
        tileset=tileset, height=height, width=width
    )
    wavefunction = Wavefunction(wavefunction)
    pyqt_plot(wavefunction=wavefunction, tileset=tileset)


def plot_completely_undetermined_simple():
    height = 7
    width = 10
    tileset = simple_tileset_factory()
    wavefunction = generate_undertermined_wavefunction(
        tileset=tileset, height=height, width=width
    )
    wavefunction = Wavefunction(wavefunction)
    pyqt_plot(wavefunction=wavefunction, tileset=tileset)


def main():

    # plot_example_pyqt_2()
    # plot_completely_undetermined_coast()
    plot_completely_undetermined_simple()


if __name__ == "__main__":

    main()
