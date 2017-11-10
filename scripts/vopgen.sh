#!/bin/bash
source $HOME/cmrr_venv/bin/activate
XF_PROJECT='/mnt/Data/XFdtd_Results/SG_Head_Coil_MRT.xf'

if [ ! -d "${XF_PROJECT}" ]; then
    echo "Could not find ${XF_PROJECT}"
    exit
else
    VOPGEN_OUT_DIR=${XF_PROJECT}/Export/Vopgen
    if [ ! -d "${VOPGEN_OUT_DIR}" ]; then
	mkdir -p ${VOPGEN_OUT_DIR}
    fi
    
    python ../xfwriter/vopgen/vopgen.py \
        --xf_project=${XF_PROJECT} \
        --export_dir=${VOPGEN_OUT_DIR} \
        --origin='[0.0, 0.0, 0.0625]' \
        --lengths='[0.325, 0.325, 0.325]' \
        --deltas='[0.002, 0.002, 0.002]'
fi

deactivate
