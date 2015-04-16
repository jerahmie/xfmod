#!/usr/bin/env python
"""
Test voxelmod
"""

import voxelmod

# create voxel metadata info from file
a = voxelmod.VoxelInfo()
a.loadVoxelInfo('voxelmod/Duke_34y_V5_2mm.txt')
a.printVoxelInfo()

b = voxelmod.VoxelData(a)
b.loadVoxelData('voxelmod/Duke_34y_V5_2mm.raw')
b.plotVoxelData()
print("Success!")


print(b._voxelInfo.material(0))
