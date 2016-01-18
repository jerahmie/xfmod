#!/usr/bin/env python3
"""
Reduce the number of materials in a voxel object according to map file.
"""
from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)

import sys, os
from os.path import pardir, sep
sys.path.append(os.path.realpath(os.path.dirname(os.path.realpath(__file__)) +
                                 sep + pardir ))
from virtual_population import *
from reduced_voxel import ReduceVoxel

voxelMapFile = os.path.realpath(os.getcwd() + sep + 'material_map_4.txt' )
fullMaterialInfoFile = os.path.realpath('/mnt/DATA/itis_Virtual_Family/Duke_Head_Fixed_Z/Duke_Head_34y_V5_2mm.txt' )
fullMaterialDataFile = os.path.realpath('/mnt/DATA/itis_Virtual_Family/Duke_Head_Fixed_Z/Duke_Head_34y_V5_2mm.raw' )

voxelReader = VirtualPopulationReader()
voxelReader.loadInfo(fullMaterialInfoFile)
voxelReader.loadData(fullMaterialDataFile)


fourMatVoxelWriter = VirtualPopulationWriter()
fourMatVoxelWriter.voxelModel = ReduceVoxel(voxelMapFile, voxelReader.voxelModel).voxelModel        
fourMatVoxelWriter.voxelModel.name = 'test'
fourMatVoxelWriter.writeVoxelToFile()
