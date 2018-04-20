#!/bin/bash
source $HOME/cmrr_venv/bin/activate
#XF_PROJECT='/mnt/Data/XFdtd_Projects/pHCP_MRS_MRT.xf'
#XF_PROJECT='/mnt/Data/XFdtd_Results/pHCP_MRS_Duke_Head_2mm.xf'
XF_PROJECT='/mnt/d/XFdtd_Projects/VTOC48_Duke_Head_2mm_quick.xf'
EXPORT_DIR=$XF_PROJECT/Export
if [ ! -d $EXPORT_DIR ]; then
    mkdir $EXPORT_DIR
fi
origin='[0.0, 0.0, 0.0]'
lengths='[0.3, 0.3, 0.3]'
dx='[0.002, 0.002, 0.002]'
simIds={1..8}
runId=1
net_input_power=1.0
for simId in {1..8}; do
    echo $simId
    python ../xfwriter/xf_griddata_writer_uniform.py \
	--xf_project=${XF_PROJECT} \
	--export_file=$EXPORT_DIR/ld_ch"$simid"_grid.mat \
	--sim=$simId \
	--run=$runId \
	--origin="${origin}" \
	--lengths="${lengths}" \
	--deltas="${dx}"

    python ../xfwriter/xf_field_writer_uniform.py \
	--xf_project=${XF_PROJECT} \
	--export_file=$EXPORT_DIR/ld_ch"$simid"_B.mat \
	--field=B \
	--sim=$simId \
	--run=$runId \
	--origin="${origin}" \
	--lengths="${lengths}" \
	--deltas="${dx}" \
	--net_input_power=${net_input_power}

    python ../xfwriter/xf_field_writer_uniform.py \
	--xf_project=${XF_PROJECT} \
	--export_file=$EXPORT_DIR/ld_ch"$simid"_E.mat \
	--field=E \
	--sim=$simId \
	--run=$runId \
	--origin="${origin}" \
	--lengths="${lengths}" \
	--deltas="${dx}" \
	--net_input_power=${net_input_power}
done

# cleanup and exit virtualenv
deactivate
