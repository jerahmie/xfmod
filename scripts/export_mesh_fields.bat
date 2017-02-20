@echo off
set XF_PROJECT="F:\7T_Dipole.xf"
set SIMID=1
set RUNID=1
set ORIGIN="[0.300, 0.160, 0.128]"
set LENGTHS="[0.256, 0.256, 0.256]"
set DELTAS="[0.002, 0.002, 0.002]"
set NET_INPUT_POWER="1.0"

rem --------------------------------------------------------------------------
rem Get XF project name from XF_PROJECT string
for %%i in ("%XF_PROJECT%") do (
set XF_PROJECT_NAME=%%~ni
) 

set EXPORT_DIR=%XF_PROJECT%\Export
if  not exist %EXPORT_DIR% (
mkdir %EXPORT_DIR%
)
echo "Material properties export and regrid"

python ..\xfwriter\xf_griddata_writer_uniform.py^
 --xf_project=%XF_PROJECT% ^
 --export_file=%EXPORT_DIR%\%XF_PROJECT_NAME%_uniform_grid.mat ^
 --sim=%SIMID% ^
 --run=%RUNID% ^
 --origin=%ORIGIN% ^
 --lengths=%LENGTHS% ^
 --deltas=%DELTAS%

echo "B-field export and regrid"

python ..\xfwriter\xf_field_writer_uniform.py ^
 --xf_project=%XF_PROJECT% ^
 --export_file=%EXPORT_DIR%\%XF_PROJECT_NAME%_uniform_B.mat ^
 --field=B ^
 --sim=%SIMID% ^
 --run=%RUNID% ^
 --origin=%ORIGIN% ^
 --lengths=%LENGTHS% ^
 --deltas=%DELTAS% ^
 --net_input_power=%NET_INPUT_POWER%

echo "E-field export and regrid"

python ..\xfwriter\xf_field_writer_uniform.py^
 --xf_project=%XF_PROJECT% ^
 --export_file=%EXPORT_DIR%\%XF_PROJECT_NAME%_uniform_E.mat ^
 --field=E ^
 --sim=%SIMID% ^
 --run=%RUNID% ^
 --origin=%ORIGIN% ^
 --lengths=%LENGTHS% ^
 --deltas=%DELTAS% ^
 --net_input_power=%NET_INPUT_POWER%

PAUSE
