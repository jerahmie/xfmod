@echo off
set XF_PROJECT="D:\XFdtd_Test_Projects\Simple_Loop_MRT_setup.xf"

set EXPORT_DIR=Export
if  not exist %EXPORT_DIR% (
mkdir %EXPORT_DIR%
)

set SIMID=2
set RUNID=1
set ORIGIN="[0.0, 0.0, 0.0]"
set LENGTHS="[0.256, 0.256, 0.256]"
set DELTAS="[0.002, 0.002, 0.002]"

echo "Material properties export and regrid"

python ..\xfwriter\xf_griddata_writer_uniform.py^
 --xf_project=%XF_PROJECT% ^
 --export_file=%EXPORT_DIR%\Simple_loop_MRT_grid.mat ^
 --sim=%SIMID% ^
 --run=%RUNID% ^
 --origin=%ORIGIN% ^
 --lengths=%LENGTHS% ^
 --deltas=%DELTAS%

echo "B-field export and regrid"

python ..\xfwriter\xf_field_writer_uniform.py ^
 --xf_project=%XF_PROJECT% ^
 --export_file=%EXPORT_DIR%\Simple_loop_MRT_B.mat ^
 --field=B ^
 --sim=%SIMID% ^
 --run=%RUNID% ^
 --origin=%ORIGIN% ^
 --lengths=%LENGTHS% ^
 --deltas=%DELTAS%

echo "E-field export and regrid"

python ..\xfwriter\xf_field_writer_uniform.py^
 --xf_project=%XF_PROJECT% ^
 --export_file=%EXPORT_DIR%\Simple_loop_MRT_E.mat ^
 --field=E ^
 --sim=%SIMID% ^
 --run=%RUNID% ^
 --origin=%ORIGIN% ^
 --lengths=%LENGTHS% ^
 --deltas=%DELTAS%
