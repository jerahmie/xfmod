#!/usr/bin/env python
"""
Plot a voxel file.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import sys, os.path, ntpath
import voxelmod
import matplotlib.pyplot as plt

def usage():
    print()
    print('Usage: python plot_voxel.py [voxel_file]')
    print('  voxel_file: voxel file name with or without file name extension')
    print()
    print('Example: python plot_voxel.py my_voxelfile.raw')
    print()
    
def main():
    if len(sys.argv) != 2:
        usage()
    else:
        filePath, fileName = ntpath.split(sys.argv[1])

        fileNameBase = os.path.splitext(fileName)[0]
        
        voxelInfoFileName = os.path.join(filePath, fileNameBase + '.txt')
        voxelDataFileName = os.path.join(filePath, fileNameBase + '.raw')
        
        if os.path.exists(voxelInfoFileName) and \
           os.path.exists(voxelDataFileName):
            voxelInfo = voxelmod.VoxelInfo()
            voxelInfo.loadVoxelInfo(voxelInfoFileName)
            voxelInfo.printVoxelInfo()
                
            voxelData = voxelmod.VoxelData(voxelInfo)
            voxelData.loadVoxelData(voxelDataFileName)
            voxelData.plotVoxelData()
        else:
            print('Could not find files: ',
                  voxelInfoFileName, ' or ',
                  voxelDataFileName )

if __name__ == "__main__":
    main()
