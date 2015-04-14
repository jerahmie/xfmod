"""
Test voxelmod
"""

from voxelmod import *

f = open('voxelmod/Duke_34y_V5_2mm.txt', 'r')
a = voxelmod.VoxelInfo(f)
a.loadVoxelInfo()

print("Success!")
