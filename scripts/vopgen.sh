#!/bin/bash
source $HOME/cmrr_venv/bin/activate
#XF_PROJECT=$1
XF_PROJECT='/run/media/jerahmie/Scratch/Loop_Dipole_array_SAR.xf'

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
        --origin='[0.317, 0.150, 0.1375]' \
        --lengths='[0.275, 0.300, 0.275]' \
        --deltas='[0.002, 0.002, 0.002]'
fi

deactivate
