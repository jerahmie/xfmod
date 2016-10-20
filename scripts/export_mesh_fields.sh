#!/bin/bash
XF_PROJECT='/mnt/DATA/XFdtd_Test_Projects/Simple_Loop_MRT_setup.xf'
SIMID=2
RUNID=1

#python3 ../xfwriter/xf_griddata_writer_uniform.py --xf_project=${XF_PROJECT} \
#    --export_file='Simple_loop_MRT_grid.mat' --sim=$SIMID --run=$RUNID \
#    --origin='[0.0, 0.0, 0.0]' \
#    --lengths='[0.256, 0.256, 0.256]' --deltas='[0.002, 0.002, 0.002]'

python3 ../xfwriter/xf_field_writer_uniform.py --xf_project=${XF_PROJECT} \
    --export_file='Simple_loop_MRT_B.mat' --sim=$SIMID --run=$RUNID \
    --field=B --origin='[0.0, 0.0, 0.0]' \
    --lengths='[0.256, 0.256, 0.256]' --deltas='[0.002, 0.002, 0.002]'

python3 ../xfwriter/xf_field_writer_uniform.py --xf_project=${XF_PROJECT} \
    --export_file='Simple_loop_MRT_E.mat' --sim=$SIMID --run=$RUNID \
    --field=E --origin='[0.0, 0.0, 0.0]' \
    --lengths='[0.256, 0.256, 0.256]' --deltas='[0.002, 0.002, 0.002]'
