#!/bin/bash
XF_PROJECT=$1
#XF_PROJECT='/mnt/DATA/XFdtd_Test_Projects/Simple_Loop.xf'
#XF_PROJECT='/Data/CMRR/xfmod/Test_Data/Test_Coil.xf'
###VOPGEN_OUT_DIR='/Data/CMRR/output'
if [ -d "${XF_PROJECT}" ]; then
    VOPGEN_OUT_DIR=${XF_PROJECT}/Export/Vopgen
    if [ ! -d "${VOPGEN_OUT_DIR}" ]; then
	mkdir -p ${VOPGEN_OUT_DIR}
    fi
    
    python3 ../xfwriter/vopgen/vopgen.py \
        --xf_project=${XF_PROJECT} \
        --export_dir=${VOPGEN_OUT_DIR} \
        --origin='[0.0, 0.0, 0.044]' \
        --lengths='[0.256, 0.256, 0.256]' \
        --deltas='[0.002, 0.002, 0.002]'
fi
