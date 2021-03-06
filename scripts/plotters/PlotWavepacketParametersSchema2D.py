#!/usr/bin/env python
r"""The WaveBlocks Project

Plot the evolution of the parameters :math:`Pi_i = (q, p, Q, P, S)`
of a homogeneous or inhomogeneous Hagedorn wavepacket during the
time propagation.

@author: R. Bourquin
@copyright: Copyright (C) 2012, 2014, 2016 R. Bourquin
@license: Modified BSD License
"""

import argparse
import os
from numpy import array, linspace, dot, sin, cos, pi, real, where, nan, isnan
from matplotlib.pyplot import figure, close

from WaveBlocksND import IOManager
from WaveBlocksND import GlobalDefaults as GLD
from WaveBlocksND.Interface import GraphicsDefaults as GD


def read_data_homogeneous(iom, blockid=0):
    r"""
    :param iom: An :py:class:`IOManager` instance providing the simulation data.
    :param blockid: The data block from which the values are read.
    """
    parameters = iom.load_parameters()
    timegrid = iom.load_wavepacket_timegrid(blockid=blockid)
    dt = parameters["dt"] if "dt" in parameters else 1.0
    # Filter
    time = timegrid * dt
    time = where(timegrid < 0, nan, time)

    Pi = iom.load_wavepacket_parameters(blockid=blockid)
    qhist, phist, Qhist, Phist, Shist = Pi

    # The Dimension D, we know that q has shape (#timesteps, D, 1)
    D = qhist.shape[1]
    if not D == 2:
        raise NotImplementedError("Trajectory plotting implemented only for 2D wavepackets")

    return (time,
            [real(qhist.reshape((-1, D)))],
            [real(phist.reshape((-1, D)))],
            [Qhist.reshape((-1, D, D))],
            [Phist.reshape((-1, D, D))],
            [Shist.reshape((-1, 1))])


def read_data_inhomogeneous(iom, blockid=0):
    r"""
    :param iom: An :py:class:`IOManager` instance providing the simulation data.
    :param blockid: The data block from which the values are read.
    """
    parameters = iom.load_parameters()
    timegrid = iom.load_wavepacket_timegrid(blockid=blockid)
    dt = parameters["dt"] if "dt" in parameters else 1.0
    # Filter
    time = timegrid * dt
    time = where(timegrid < 0, nan, time)

    Pis = iom.load_inhomogwavepacket_parameters(blockid=blockid)

    # The Dimension D, we know that q_0 has shape (#timesteps, D, 1)
    D = Pis[0][0].shape[1]
    if not D == 2:
        raise NotImplementedError("Trajectory plotting implemented only for 2D wavepackets")

    # List with Pi time evolutions
    Phist = []
    Qhist = []
    Shist = []
    phist = []
    qhist = []

    for q, p, Q, P, S in Pis:
        qhist.append(real(q.reshape((-1, D))))
        phist.append(real(p.reshape((-1, D))))
        Qhist.append(Q.reshape((-1, D, D)))
        Phist.append(P.reshape((-1, D, D)))
        Shist.append(S.reshape((-1, 1)))

    return (time, qhist, phist, Qhist, Phist, Shist)


def plot_parameters(data, index=0, path='.'):
    r"""Plot the data parameters :math:`(q,p,Q,P,S)` over time.
    For each new `index` we start a new figure. This allows plotting
    several time evolutions to the same figure
    """
    print("Plotting the parameters of data block '%s'" % index)

    time, qhist, phist, Qhist, Phist, Shist = data
    vals = ~isnan(time)

    r = 1.0
    theta = linspace(0, 2 * pi, 64)
    circle = array([r * cos(theta), r * sin(theta)])

    # Plot the 2D trajectory of the parameters q and p
    fig = figure()
    ax = fig.gca()
    for qitem, Qitem in zip(qhist, Qhist):
        for q, Q, vi, in zip(qitem, Qitem, vals):
            if vi:
                C = real(q.reshape((-1, 1)) + dot(Q, circle))
                ax.plot(q[0], q[1], "bo")
                ax.plot(C[0, :], C[1, :], "b-", alpha=0.5)

    ax.set_xlabel(r"$q_x(t)$")
    ax.set_ylabel(r"$q_y(t)$")
    ax.grid(True)
    ax.set_aspect("equal")
    ax.set_title(r"Schematic evolution of $q$ and $Q$")
    fig.savefig(os.path.join(path, "wavepacket_parameters_schema_pos_block"+str(index)+GD.output_format))
    close(fig)


    fig = figure()
    ax = fig.gca()
    for pitem, Pitem in zip(phist, Phist):
        for p, P, vi in zip(pitem, Pitem, vals):
            if vi:
                C = real(p.reshape((-1, 1)) + dot(P, circle))
                ax.plot(p[0], p[1], "bo")
                ax.plot(C[0, :], C[1, :], "b-", alpha=0.5)
    ax.set_xlabel(r"$p_x(t)$")
    ax.set_ylabel(r"$p_y(t)$")
    ax.grid(True)
    ax.set_aspect("equal")
    ax.set_title(r"Schematic evolution of $p$ and $P$")
    fig.savefig(os.path.join(path, "wavepacket_parameters_schema_mom_lock"+str(index)+GD.output_format))
    close(fig)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--datafile",
                        type = str,
                        help = "The simulation data file",
                        nargs = "?",
                        default = GLD.file_resultdatafile)

    parser.add_argument("-b", "--blockid",
                        type = str,
                        help = "The data block to handle",
                        nargs = "*",
                        default = ["all"])

    parser.add_argument("-r", "--resultspath",
                        type = str,
                        help = "Path where to put the results.",
                        nargs = "?",
                        default = '.')

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

    # Iterate over all blocks
    for blockid in blockids:
        print("Plotting wavepacket parameters in data block '{}'".format(blockid))

        # NOTE: Add new algorithms here

        if iom.has_wavepacket(blockid=blockid):
            plot_parameters(read_data_homogeneous(iom, blockid=blockid), index=blockid, path=resultspath)
        elif iom.has_inhomogwavepacket(blockid=blockid):
            plot_parameters(read_data_inhomogeneous(iom, blockid=blockid), index=blockid, path=resultspath)
        else:
            print("Warning: Not plotting wavepacket parameters in block '{}'".format(blockid))

    iom.finalize()
