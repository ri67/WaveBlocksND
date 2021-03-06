#!/usr/bin/env python
"""The WaveBlocks Project

Compute the eigen transformation of the simulation results given.

@author: R. Bourquin
@copyright: Copyright (C) 2012, 2013, 2014, 2016 R. Bourquin
@license: Modified BSD License
"""

import argparse
import os

from WaveBlocksND import IOManager
from WaveBlocksND import GlobalDefaults as GD

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--inputfile",
                    type = str,
                    help = "The data file to read the data from.",
                    default = GD.file_resultdatafile)

parser.add_argument("-o", "--outputfile",
                    type = str,
                    help = "The data file to write the transformed data.")

parser.add_argument("-r", "--resultspath",
                    type = str,
                    help = "Path where to put the results.",
                    nargs = "?",
                    default = '.')

args = parser.parse_args()


# Files with the simulation data
resultspath = os.path.abspath(args.resultspath)

if not os.path.exists(resultspath):
    raise IOError("The results path does not exist: {}".format(args.resultspath))

inputfile = os.path.abspath(os.path.join(args.resultspath, args.inputfile))

# No output file name given
if not args.outputfile:
    outputfile = inputfile.replace(GD.ext_resultdatafile, "") + "_eigen" + GD.ext_resultdatafile
else:
    outputfile = args.outputfile

outputfile = os.path.abspath(os.path.join(args.resultspath, outputfile))

print("Reading simulation data from the file: {}".format(inputfile))
print("Writing transformed data to the file: {}".format(outputfile))

# Read file with simulation data
iomc = IOManager()
iomc.open_file(inputfile)

iome = IOManager()
iome.create_file(outputfile)

# New file for eigen transformed data
P = iomc.load_parameters()

# Save the simulation parameters
iome.add_parameters()
iome.save_parameters(P)

# Iterate over all groups
for groupid in iomc.get_group_ids():

    # Create the group if necessary
    if groupid not in iome.get_group_ids():
        iome.create_group(groupid=groupid)

    for blockid in iomc.get_block_ids(groupid=groupid):
        print("Computing eigentransformation of data in block '{}'".format(blockid))

        # Create the block if necessary
        if blockid not in iome.get_block_ids(groupid=groupid):
            iome.create_block(blockid=blockid, groupid=groupid)

        # See if we have a wavefunction
        if iomc.has_wavefunction(blockid=blockid):
            from WaveBlocksND.Interface import EigentransformWavefunction
            EigentransformWavefunction.transform_wavefunction_to_eigen(iomc, iome, blockidin=blockid, blockidout=blockid)

        # See if we have a homogeneous wavepacket next
        if iomc.has_wavepacket(blockid=blockid):
            from WaveBlocksND.Interface import EigentransformHagedornWavepacket
            EigentransformHagedornWavepacket.transform_hawp_to_eigen(iomc, iome, blockidin=blockid, blockidout=blockid)

        # See if we have an inhomogeneous wavepacket next
        if iomc.has_inhomogwavepacket(blockid=blockid):
            from WaveBlocksND.Interface import EigentransformHagedornWavepacket
            EigentransformHagedornWavepacket.transform_inhawp_to_eigen(iomc, iome, blockidin=blockid, blockidout=blockid)

iomc.finalize()
iome.finalize()
