#!/bin/bash
source $HOME/cmrr_venv/bin/activate
XF_PROJECT='/run/media/jerahmie/Scratch/Green_Coil_10p5T_Amazon_Phantom_MRT_decoupled.xf'
EXPORT_DIR=$XF_PROJECT/Export
if [ ! -d $EXPORT_DIR ]; then
    mkdir $EXPORT_DIR
fi

n_channels = 16
runid=1
net_input_power=1.0

for simid in {1..$n_channels}; do
    python3 ../xfwriter/xf_griddata_writer_uniform.py \
	--xf_project=${XF_PROJECT} \
	--export_file=$EXPORT_DIR/ld_ch"$simid"_grid.mat \
	--sim=$simid \
	--run=$runid \
	--origin='[0.0, 0.0, 0.0625]' \
	--lengths='[0.230, 0.275, 0.215]' \
	--deltas='[0.002, 0.002, 0.002]'

    python3 ../xfwriter/xf_field_writer_uniform.py \
	--xf_project=${XF_PROJECT} \
	--export_file=$EXPORT_DIR/ld_ch"$simid"_B.mat \
	--field=B \
	--sim=$simid \
	--run=$runid \
	--origin='[0.0, 0.0, 0.0625]' \
	--lengths='[0.230, 0.275, 0.215]' \
	--deltas='[0.002, 0.002, 0.002]' \
	--net_input_power=${net_input_power}

    python3 ../xfwriter/xf_field_writer_uniform.py \
	--xf_project=${XF_PROJECT} \
	--export_file=$EXPORT_DIR/ld_ch"$simid"_E.mat \
	--field=E \
	--sim=$simid \
	--run=$runid \
	--origin='[0.0, 0.0, 0.0625]' \
	--lengths='[0.230, 0.275, 0.215]' \
	--deltas='[0.002, 0.002, 0.002]' \
	--net_input_power=${net_input_power}
done

# cleanup and exit virtualenv
deactivate
