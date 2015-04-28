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

def isDuke(fileName):
    """
    Determines if we the model used is Duke.
    """
    if re.search(r"Duke", fileName):
        return True
    else:
        return False

VOXEL_MODEL_FILE_NAME_RE = "(Billie|Ella|Thelonious|Duke)([a-zA-Z0-9_.]*).(txt|raw)$"


# Begin Settings
voxelInfoFileName = '/mnt/DATA/itis_Virtual_Family/Virtual Family Voxel Models V1.0/Duke_34y_V5_5mm.txt'
voxelDataFileName = '/mnt/DATA/itis_Virtual_Family/Virtual Family Voxel Models V1.0/Duke_34y_V5_5mm.raw'
#voxelInfoFileName = '/mnt/DATA/itis_Virtual_Family/Virtual Family Voxel Models V1.0/Billie_11y_V2_1mm.txt'
#voxelDataFileName = '/mnt/DATA/itis_Virtual_Family/Virtual Family Voxel Models V1.0/Billie_11y_V2_1mm.raw'

# fraction of data to be saved
#dataFraction = 0.15 # Head only
dataFraction = 0.25  # 25% is a good value for head and shoulders
#dataFraction = 1.0   # entire body

# simple data descriptor to insert after model name in output file
#fileDesc = "_Fixed_Z" # for Duke when correcting Z orientation
fileDesc = "_Head"    # just head (and shoulders)

# Plot saved results?  If True, the saved voxel info will be loaded and plotted
#  for inspection.
plotSaved = False

# End Settings

# construct Output file names
filePath, fileName = ntpath.split(voxelInfoFileName)
mInfo = re.match(VOXEL_MODEL_FILE_NAME_RE, fileName)
newVoxelInfoFileName = mInfo.group(1) + fileDesc + mInfo.group(2) + ".txt"
newVoxelDataFileName = mInfo.group(1) + fileDesc + mInfo.group(2) + ".raw"

# create voxel metadata info from file
origVoxelInfo = voxelmod.VoxelInfo()
origVoxelInfo.loadVoxelInfo(voxelInfoFileName)
origVoxelInfo.printVoxelInfo()

# load voxelData based off of voxel metadata
origVoxelData = voxelmod.VoxelData(origVoxelInfo)
origVoxelData.loadVoxelData(voxelDataFileName)
if isDuke(voxelInfoFileName):
    print("Voxel Image is 'Duke'")
    origVoxelData.flipZ()
origVoxelData.voxelDataSubRegion((0,origVoxelInfo.nx),
                                 (0,origVoxelInfo.ny),
                                 (0,int(dataFraction*origVoxelInfo.nz)))

    
origVoxelData.plotVoxelData()

#prompt for save?
while True:
    save_choice = raw_input('Save the voxel data? (y/n): ')
    if save_choice == 'y':
        origVoxelData.saveVoxelInfo(newVoxelInfoFileName)
        origVoxelData.saveVoxelData(newVoxelDataFileName)

        # check the results for consistency
        if plotSaved:
            newVoxelInfo = voxelmod.VoxelInfo()
            newVoxelInfo.loadVoxelInfo(newVoxelInfoFileName)
            newVoxelInfo.printVoxelInfo()
            
            newVoxelData = voxelmod.VoxelData(newVoxelInfo)
            newVoxelData.loadVoxelData(newVoxelDataFileName)
            newVoxelData.plotVoxelData()
        
        break
        
    elif save_choice == 'n':
        break
    else:
        print("Press <y> or <n>")

    

