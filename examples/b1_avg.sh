#!/bin/bash
XF_PROJECT_DIR='/mnt/DATA/XFdtd_Results/Dipole_Coil_10p5T_Phantom.xf'
EXPORT_DIR=${XF_PROJECT_DIR}/Export
if [ -d "${EXPORT_DIR}" ]; then
    mkdir -p ${EXPORT_DIR}
fi

python3 sum_b1_total.py --xf_project=${XF_PROJECT_DIR} --sim='[1, 2, 3, 4, 5, 6, 7, 8]' --export_file="${EXPORT_DIR}/b1tx.mat"
