#!/usr/bin/env python
"""
Test voxelmod
"""

import voxelmod

a = voxelmod.VoxelInfo('voxelmod/Duke_34y_V5_2mm.txt')
a.loadVoxelInfo()
a.printVoxelInfo()
print("Success!")
