#!/usr/bin/env python
"""The WaveBlocks Project

Plot the energies of the different wavepackets as well as the sum of all energies.

@author: R. Bourquin
@copyright: Copyright (C) 2010, 2011, 2012, 2014, 2016 R. Bourquin
@license: Modified BSD License
"""

import argparse
import os
from functools import reduce
from numpy import abs, add, where, nan, nanmax, nanmin
from matplotlib.pyplot import figure, close

from WaveBlocksND import IOManager
from WaveBlocksND.Plot import legend
from WaveBlocksND import GlobalDefaults as GLD
from WaveBlocksND.Interface import GraphicsDefaults as GD


def read_all_datablocks(iom):
    """Read the data from all blocks that contain any usable data.

    :param iom: An :py:class:`IOManager` instance providing the simulation data.
    """


def read_data(iom, blockid=0):
    """
    :param iom: An :py:class:`IOManager` instance providing the simulation data.
    :param blockid: The data block from which the values are read.
    """
    if iom.has_parameters():
        parameters = iom.load_parameters()
        if "dt" in parameters:
            dt = parameters["dt"]
    else:
        dt = None

    timegridk, timegridp = iom.load_energy_timegrid(blockid=blockid)

    ekin, epot = iom.load_energy(blockid=blockid, split=True)
    # Compute the sum of all energies
    ekin.append(reduce(add, ekin))
    epot.append(reduce(add, epot))

    return (timegridk, timegridp, ekin, epot, dt)


def plot_energies(data, blockid=0, view=None, path='.'):
    print("Plotting the energies of data block '{}'".format(blockid))

    timegridk, timegridp, ekin, epot, dt = data

    if dt is None:
        xlbl = r"Timesteps $n$"
        dt = 1.0
    else:
        xlbl = r"Time $t$"

    # Filter
    timek = timegridk * dt
    timep = timegridp * dt
    timek = where(timegridk < 0, nan, timek)
    timep = where(timegridp < 0, nan, timep)

    # View
    if view[0] is None:
        view[0] = min(nanmin(timek), nanmin(timep))
    if view[1] is None:
        view[1] = max(nanmax(timek), nanmax(timep))

    # Plot the energies
    fig = figure()
    ax = fig.gca()

    # Plot the kinetic energy of the individual wave packets
    for i, kin in enumerate(ekin[:-1]):
        ax.plot(timek, kin, label=r"$E^{kin}_{%d}$" % i)

    # Plot the potential energy of the individual wave packets
    for i, pot in enumerate(epot[:-1]):
        ax.plot(timep, pot, label=r"$E^{pot}_{%d}$" % i)

    # Plot the sum of kinetic and potential energy for all wave packets
    for i, (kin, pot) in enumerate(list(zip(ekin, epot))[:-1]):
        ax.plot(timek, kin + pot, label=r"$E^{kin}_{%d}+E^{pot}_{%d}$" % (i, i))

    # Plot sum of kinetic and sum of potential energy
    ax.plot(timek, ekin[-1], label=r"$\sum_i E^{kin}_i$")
    ax.plot(timep, epot[-1], label=r"$\sum_i E^{pot}_i$")

    # Plot the overall energy of all wave packets
    ax.plot(timek, ekin[-1] + epot[-1], label=r"$\sum_i E^{kin}_i + \sum_i E^{pot}_i$")

    ax.set_xlim(view[:2])
    if None not in view[2:]:
        ax.set_ylim(view[2:])
    ax.ticklabel_format(style="sci", scilimits=(0, 0), axis="y")
    ax.grid(True)
    ax.set_xlabel(xlbl)
    legend(loc="outer right")
    ax.set_title(r"Energies of the wavepacket $\Psi$")
    fig.savefig(os.path.join(path, "energies_block" + str(blockid) + GD.output_format))
    close(fig)


    # Plot the energy drift
    e_orig = (ekin[-1] + epot[-1])[0]
    data = abs(e_orig - (ekin[-1] + epot[-1]))

    fig = figure()
    ax = fig.gca()

    ax.plot(timek, data, label=r"$|E_O^0 - \left( E_k^0 + E_p^0 \right) |$")

    ax.set_xlim(view[:2])
    ax.ticklabel_format(style="sci", scilimits=(0, 0), axis="y")
    ax.grid(True)
    ax.set_xlabel(xlbl)
    ax.set_ylabel(r"$|E_O^0 - \left( E_k^0 + E_p^0 \right) |$")
    ax.set_title(r"Energy drift of the wavepacket $\Psi$")
    fig.savefig(os.path.join(path, "energy_drift_block" + str(blockid) + "_lin" + GD.output_format))
    close(fig)


    fig = figure()
    ax = fig.gca()

    ax.semilogy(timek, data, label=r"$|E_O^0 - \left( E_k^0 + E_p^0 \right) |$")

    ax.set_xlim(view[:2])
    ax.grid(True)
    ax.set_xlabel(xlbl)
    ax.set_ylabel(r"$|E_O^0 - \left( E_k^0 + E_p^0 \right) |$")
    ax.set_title(r"Energy drift of the wavepacket $\Psi$")
    fig.savefig(os.path.join(path, "energy_drift_block" + str(blockid) + "_log" + GD.output_format))
    close(fig)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--datafile",
                        type=str,
                        help="The simulation data file",
                        nargs="?",
                        default=GLD.file_resultdatafile)

    parser.add_argument("-b", "--blockid",
                        type=str,
                        help="The data block to handle",
                        nargs="*",
                        default=["all"])

    parser.add_argument("-r", "--resultspath",
                        type=str,
                        help="Path where to put the results.",
                        nargs="?",
                        default='.')

    parser.add_argument("-t", "--trange",
                        type=float,
                        help="The plot range on the t-axis",
                        nargs=2,
                        default=[None, None])

    parser.add_argument("-v", "--vrange",
                        type=float,
                        help="The plot range on the y-axis",
                        nargs=2,
                        default=[None, None])

    args = parser.parse_args()


    # File with the simulation data
    resultspath = os.path.abspath(args.resultspath)

    if not os.path.exists(resultspath):
        raise IOError("The results path does not exist: {}".format(args.resultspath))

    datafile = os.path.abspath(os.path.join(args.resultspath, args.datafile))

    # Read file with simulation data
    iom = IOManager()
    iom.open_file(filename=datafile)

    # Which blocks to handle
    blockids = iom.get_block_ids()
    if "all" not in args.blockid:
        blockids = [bid for bid in args.blockid if bid in blockids]

    # The axes rectangle that is plotted
    view = args.trange + args.vrange

    # Iterate over all blocks
    for blockid in iom.get_block_ids():
        print("Plotting energies in data block '{}'".format(blockid))

        if iom.has_energy(blockid=blockid):
            plot_energies(read_data(iom, blockid=blockid), blockid=blockid, view=view, path=resultspath)
        else:
            print("Warning: Not plotting energies in block '{}'".format(blockid))

    iom.finalize()
