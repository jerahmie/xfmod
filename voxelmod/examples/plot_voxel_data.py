#!/usr/bin/env python
"""
Test voxelmod
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import sys, os.path, ntpath
import re
import voxelmod
import matplotlib.pyplot as plt

VOXEL_MODEL_FILE_NAME_RE = "(Billie|Ella|Thelonious|Duke)([a-zA-Z0-9_.]*).(txt|raw)$"


# voxelInfoFileName = '/mnt/DATA/itis_Virtual_Family/Virtual Family Voxel Models V1.0/Duke_34y_V5_1mm.txt'
# voxelDataFileName = '/mnt/DATA/itis_Virtual_Family/Virtual Family Voxel Models V1.0/Duke_34y_V5_1mm.raw'
voxelInfoFileName = 'Duke_34y_V5_2mm.txt'
voxelDataFileName = 'Duke_34y_V5_2mm.raw'
#voxelInfoFileName = 'Duke_Head_34y_V5_2mm.txt'
#voxelDataFileName = 'Duke_Head_34y_V5_2mm.raw'


# construct 
filePath, fileName = ntpath.split(voxelInfoFileName)
mInfo = re.match(VOXEL_MODEL_FILE_NAME_RE, fileName)
newVoxelInfoFileName = mInfo.group(1) + "_Head" + mInfo.group(2) + ".txt"
newVoxelDataFileName = mInfo.group(1) + "_Head" + mInfo.group(2) + ".raw"

# create voxel metadata info from file
origVoxelInfo = voxelmod.VoxelInfo()
origVoxelInfo.loadVoxelInfo(voxelInfoFileName)
origVoxelInfo.printVoxelInfo()

# load voxelData based off of voxel metadata
origVoxelData = voxelmod.VoxelData(origVoxelInfo)
origVoxelData.loadVoxelData(voxelDataFileName)
origVoxelData.voxelDataSubRegion((0,origVoxelInfo.nx),
                                 (0,origVoxelInfo.ny),
                                 (int(0.75*origVoxelInfo.nz),origVoxelInfo.nz))
origVoxelData.plotVoxelData()

    


