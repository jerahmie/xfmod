#!/bin/bash
#XF_PROJECT='/mnt/DATA/XFdtd_Test_Projects/Simple_Loop.xf'
XF_PROJECT='/Data/CMRR/xfmod/Test_Data/Test_Coil.xf'
VOPGEN_OUT_DIR='/Data/CMRR/output'

python3 ../xfwriter/vopgen/vopgen.py \
        --xf_project=${XF_PROJECT} \
        --export_dir=${VOPGEN_OUT_DIR} \
        --origin='[0.0, 0.0, 0.044]' \
        --lengths='[0.256, 0.256, 0.256]' \
        --deltas='[0.002, 0.002, 0.002]'
