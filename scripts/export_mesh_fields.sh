#!/bin/bash
XF_PROJECT='/mnt/DATA/XFdtd_Test_Projects/Simple_Loop_MRT_setup.xf'
EXPORT_DIR=$XF_PROJECT/Export
if [ ! -d $EXPORT_DIR ]; then
    mkdir $EXPORT_DIR
fi
SIMID=2
RUNID=1
NET_INPUT_POWER=1.0
python3 ../xfwriter/xf_griddata_writer_uniform.py --xf_project=${XF_PROJECT} \
    --export_file=$EXPORT_DIR/Simple_loop_MRT_grid.mat \
    --sim=$SIMID \
    --run=$RUNID \
    --origin='[0.0, 0.0, 0.0]' \
    --lengths='[0.256, 0.256, 0.256]' \
    --deltas='[0.002, 0.002, 0.002]' \
    --net_input_power=${NET_INPUT_POWER}

python3 ../xfwriter/xf_field_writer_uniform.py --xf_project=${XF_PROJECT} \
    --export_file=$EXPORT_DIR/Simple_loop_MRT_B.mat \
    --field=B \
    --sim=$SIMID \
    --run=$RUNID \
    --origin='[0.0, 0.0, 0.0]' \
    --lengths='[0.256, 0.256, 0.256]' \
    --deltas='[0.002, 0.002, 0.002]' \
    --net_input_power=${NET_INPUT_POWER}

python3 ../xfwriter/xf_field_writer_uniform.py --xf_project=${XF_PROJECT} \
    --export_file=$EXPORT_DIR/Simple_loop_MRT_E.mat \
    --field=E \
    --sim=$SIMID \
    --run=$RUNID \
    --origin='[0.0, 0.0, 0.0]' \
    --lengths='[0.256, 0.256, 0.256]' \
    --deltas='[0.002, 0.002, 0.002]' \
    --net_input_power=${NET_INPUT_POWER}
