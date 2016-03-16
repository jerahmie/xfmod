#!/bin/bash


python3 export_fields_uniform.py --xf_project='../Test_Data/Test_Coil.xf' --export_file='test_B_0.mat' --sim=1 --run=1 --field=B --origin='[0.0, 0.0, 0.0]' --lengths='[0.256, 0.256, 0.256]' --deltas='[0.002, 0.002, 0.002]'
