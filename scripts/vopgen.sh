#!/bin/bash
source $HOME/cmrr_venv/bin/activate
XF_PROJECT='/mnt/Data/XFdtd_Projects/Stripline_10p5T_MRT_test_decoupling3.xf'

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
        --origin='[0.0, 0.0, 0.0]' \
        --lengths='[0.3, 0.3, 0.35]' \
        --deltas='[0.002, 0.002, 0.002]'
fi

deactivate
