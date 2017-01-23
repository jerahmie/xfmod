#!/bin/bash
source $HOME/cmrr_venv/bin/activate
#XF_PROJECT='/mnt/DATA/XFdtd_Results/BL_Frontal_7T_Duke_Head_2mm.xf'
XF_PROJECT='/run/media/jerahmie/Scratch/Scratch/Loop_Dipole_10p5T_V2_Phantom.xf'
EXPORT_DIR=$XF_PROJECT/Export
if [ ! -d $EXPORT_DIR ]; then
    mkdir $EXPORT_DIR
fi

runid=1
net_input_power=1.0

for simid in {1..16}; do
    python3 ../xfwriter/xf_griddata_writer_uniform.py \
	--xf_project=${XF_PROJECT} \
	--export_file=$EXPORT_DIR/ld_ch"$simid"_grid.mat \
	--sim=$simid \
	--run=$runid \
	--origin='[0.0, 0.0, -0.117]' \
	--lengths='[0.256, 0.256, 0.256]' \
	--deltas='[0.002, 0.002, 0.002]'

    python3 ../xfwriter/xf_field_writer_uniform.py \
	--xf_project=${XF_PROJECT} \
	--export_file=$EXPORT_DIR/ld_ch"$simid"_B.mat \
	--field=B \
	--sim=$simid \
	--run=$runid \
	--origin='[0.0, 0.0, -0.117]' \
	--lengths='[0.256, 0.256, 0.256]' \
	--deltas='[0.002, 0.002, 0.002]' \
	--net_input_power=${net_input_power}

    python3 ../xfwriter/xf_field_writer_uniform.py \
	--xf_project=${XF_PROJECT} \
	--export_file=$EXPORT_DIR/ld_ch"$simid"_E.mat \
	--field=E \
	--sim=$simid \
	--run=$runid \
	--origin='[0.0, 0.0, -0.117]' \
	--lengths='[0.256, 0.256, 0.256]' \
	--deltas='[0.002, 0.002, 0.002]' \
	--net_input_power=${net_input_power}
done

# cleanup and exit virtualenv
deactivate
