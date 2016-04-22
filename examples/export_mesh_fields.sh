#!/bin/bash
XF_PROJECT='/mnt/DATA/XFdtd_Test_Projects/Simple_Loop.xf'
SIMID=83
RUNID=1

#python3 export_grid_data_uniform.py --xf_project=${XF_PROJECT} \
#    --export_file='Simple_loop_no_mesh_grid.mat' --sim=$SIMID --run=$RUNID \
#    --origin='[0.0, 0.0, 0.044]' \
#    --lengths='[0.256, 0.256, 0.256]' --deltas='[0.002, 0.002, 0.002]'

python3 export_fields_uniform.py --xf_project=${XF_PROJECT} \
    --export_file='Simple_loop_with_mesh_B.mat' --sim=$SIMID --run=$RUNID \
    --field=B --origin='[0.0, 0.0, 0.044]' \
    --lengths='[0.256, 0.256, 0.256]' --deltas='[0.002, 0.002, 0.002]'
