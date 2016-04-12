#!/bin/bash
#xf_project_dir='/mnt/DATA/XFdtd_Results/Green_Coil_7T_Duke_Head_2mm.xf'
xf_project_dir='/mnt/DATA/XFdtd_Projects/HW_Visual_Cortex_Coil_7T_Hugo.xf'
z_value='-0.0184'
#z_value='-0.2'
xf_project_name=`basename -s .xf ${xf_project_dir}`
echo XF Project Name: $xf_project_name
export_dir=${xf_project_dir}/Export
if [ ! -d "${export_dir}" ]; then
    mkdir -p ${export_dir}
fi

sim_string='['
for sim_dir in $xf_project_dir/Simulations/*
do
    next_sim=`basename $sim_dir | sed 's/^0*//'`
    sim_string="$sim_string$next_sim, "
done
sim_string="${sim_string::-2}]"
sim_string="[65]"
echo $sim_string


# Add B1 
python3 sum_b1_total.py --xf_project=${xf_project_dir} --sim="$sim_string" --export_file="${export_dir}/${xf_project_name}_b1tx.mat"
# plot results
python3 plot_sum_b1_total.py "${export_dir}/${xf_project_name}_b1tx.mat" ${z_value}
