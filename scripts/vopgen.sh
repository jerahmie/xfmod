#!/bin/bash
#XF_PROJECT=$1
#XF_PROJECT='/mnt/DATA/XFdtd_Results/Green_Coil_7T_Duke_Head_2mm.xf' 
#XF_PROJECT='/Data/CMRR/xfmod/Test_Data/Test_Coil.xf'
XF_PROJECT='/run/media/jerahmie/Scratch/Green_Coil_10p5T_Amazon_Phantom_MRT_decoupled.xf'

if [ ! -d "${XF_PROJECT}" ]; then
    echo "Could not find ${XF_PROJECT}"
    exit
else
    VOPGEN_OUT_DIR=${XF_PROJECT}/Export/Vopgen
    if [ ! -d "${VOPGEN_OUT_DIR}" ]; then
	mkdir -p ${VOPGEN_OUT_DIR}
    fi
    
    python3 ../xfwriter/vopgen/vopgen.py \
        --xf_project=${XF_PROJECT} \
        --export_dir=${VOPGEN_OUT_DIR} \
        --origin='[0.0, 0.0, 0.0625]' \
        --lengths='[0.230, 0.275, 0.215]' \
        --deltas='[0.002, 0.002, 0.002]'
fi
