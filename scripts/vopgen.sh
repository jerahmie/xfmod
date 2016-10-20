#!/bin/bash
#XF_PROJECT=$1
XF_PROJECT='/mnt/DATA/XFdtd_Results/Green_Coil_7T_Duke_Head_2mm.xf' 
#XF_PROJECT='/Data/CMRR/xfmod/Test_Data/Test_Coil.xf' 

if [ -d "${XF_PROJECT}" ]; then
    VOPGEN_OUT_DIR=${XF_PROJECT}/Export/Vopgen
    if [ ! -d "${VOPGEN_OUT_DIR}" ]; then
	mkdir -p ${VOPGEN_OUT_DIR}
    fi
    
    python3 ../xfwriter/vopgen/vopgen.py \
        --xf_project=${XF_PROJECT} \
        --export_dir=${VOPGEN_OUT_DIR} \
        --origin='[0.0, 0.0, 0.08]' \
        --lengths='[0.256, 0.256, 0.256]' \
        --deltas='[0.002, 0.002, 0.002]'
fi
