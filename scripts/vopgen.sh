#!/bin/bash
source $HOME/cmrr_venv/bin/activate
#XF_PROJECT='/mnt/Data/XFdtd_Projects/Stripline_10p5T_MRT_no_feeds.xf'
XF_PROJECT='/mnt/Data/XFdtd_Projects/10p5T_8CH_EndLoadedDipole-4-13-2018.xf'

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
        --origin='[-0.128175, 0.0, 0.0575]' \
        --lengths='[0.335, 0.335, 0.465]' \
        --deltas='[0.002, 0.002, 0.002]'
fi

deactivate
