"""
Parse XFdtd geometry.input file and populate a data structure with materials
and properties.
"""

# Ensure python 2 and 3 compatibility
from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)

import re
import os
from xfmod.xfutils import xf_run_id_to_str, xf_sim_id_to_str
from xfmod.xfgeomod import XFGridData, XFMaterial

# Regex expressions
_MAT_FREESPACE_PATTERN = r'^begin_<electricfreespace> ' + \
                         r'(ElectricFreeSpace)\n' + \
                         r'material_number (\d+)\n' + \
                         r'conductivity ([\d\-eE.]*)\n' + \
                         r'permittivity ([\d\-eE.]*)\n' + \
                         r'density ([\d\-eE.]*)\n' + \
                         r'water_ratio ([\d\-eE.]*)\n' + \
                         r'end_<electricfreespace>'

_MAT_PEC_PATTERN = r'^begin_<electricperfectconductor> ' + \
                   r'(ElectricPerfectConductor)\n' + \
                   r'material_number (\d+)\n' + \
                   r'end_<electricperfectconductor>'
#r'(["\w\s\d\-\(\)]+)\s*\n' + \
_MAT_NORMALELECTRIC_PATTERN = r'^begin_<normal_electric>\s*' + \
                              r'(.*)\n' + \
                              r'material_number (\d+)\n' + \
                              r'conductivity ([\d\-eE.]*)\n'+ \
                              r'uncorrected_conductivity ' + \
                              r'([\d\-eE.]*)\n' + \
                              r'permittivity ([\d\-eE.]*)\n' + \
                              r'(effectiveConductivity\s*' +\
                              r'[\d\-eE.]*\n)?' + \
                              r'(effectiveUncorrectedConductivity\s*' +\
                              r'[\d\-eE.]*\n)?' + \
                              r'(effectiveRelativePermittivity\s*' + \
                              r'[\d\-eE.]*\n)?' + \
                              r'density ([\d\-eE.]*)\n' + \
                              r'water_ratio ([\d\-eE.]*)\nbegin_' + \
                              r'<TemperatureRiseMaterial' + \
                              r'Parameters>\s*\n' + \
                              r'heat_capacity ([\d\-eE.]*)\n' + \
                              r'thermal_conductivity ([\d\-eE.]*)\n' + \
                              r'perfusion_rate ([\d\-eE.]*)\n' + \
                              r'metabolic_heat ([\d\-eE.]*)\n' + \
                              r'tissue (\d+)\nend_' + \
                              r'<TemperatureRiseMaterialParameters>' + \
                              r'\s*\nend_<normal_electric>'

_GRID_DEFINITION = r'^begin_<GridDefinition>\s*\n' + \
                   r'GridOriginInMeters\s*' + \
                   r'([\d\-.]+) ([\d\-.]+) ([\d\-.]+)\n' + \
                   r'NumberOfCellsInX (\d+)\s*\n' + \
                   r'NumberOfCellsInY (\d+)\s*\n' + \
                   r'NumberOfCellsInZ (\d+)\s*\n' + \
                   r'end_<GridDefinition>'

_GRID_BEGIN_DELX = r'begin_<DelX>\s*'
_GRID_END_DELX = r'end_<DelX>\s*'
_GRID_BEGIN_DELY = r'begin_<DelY>\s*'
_GRID_END_DELY = r'end_<DelY>\s*'
_GRID_BEGIN_DELZ = r'begin_<DelZ>\s*'
_GRID_END_DELZ = r'end_<DelZ>\s*'
_GRID_DELTA = r'(\d*)\s([\d\-.]*)\n'

class XFGeometry(object):
    """A class to hold coil geometry info."""
    NAME = 0
    MATERIAL_NUMBER = 1
    CONDUCTIVITY = 2
    PERMITTIVITY = 4
    DENSITY = 8
    WATER_RATIO = 9
    HEAT_CAPACITY = 10
    THERMAL_CONDUCTIVITY = 11
    PERFUSION_RATE = 12
    METABOLIC_HEAT = 13
    TISSUE = 14

    def __init__(self, xf_project_dir, sim_id, run_id):
        # compile patterns
        self._mat_free_space = re.compile(_MAT_FREESPACE_PATTERN, \
                                              re.MULTILINE)
        self._mat_pec = re.compile(_MAT_PEC_PATTERN, re.MULTILINE)
        self._mat_norm_electric = re.compile(_MAT_NORMALELECTRIC_PATTERN,\
                                            re.MULTILINE)
        self._grid_definition = re.compile(_GRID_DEFINITION, \
                                           re.MULTILINE)
        self._begin_delx = re.compile(_GRID_BEGIN_DELX)
        self._end_delx = re.compile(_GRID_END_DELX)
        self._begin_dely = re.compile(_GRID_BEGIN_DELY)
        self._end_dely = re.compile(_GRID_END_DELY)
        self._begin_delz = re.compile(_GRID_BEGIN_DELZ)
        self._end_delz = re.compile(_GRID_END_DELZ)
        self._grid_delta = re.compile(_GRID_DELTA, re.MULTILINE)

        # file info
        self._geometry_input_file_path = os.path.join(xf_project_dir,
                                                      r'Simulations',
                                                      xf_sim_id_to_str(sim_id),
                                                      xf_run_id_to_str(run_id),
                                                      r'geometry.input')

        # geometry info
        self._geom_info = ''
        self._materials = []
        self.grid_data = XFGridData()
        self._load_grid_data()

    def load_materials(self):
        """Load materials from material.input."""
        if os.path.exists(self._geometry_input_file_path):
            self._materials = []
            file_handle = open(self._geometry_input_file_path, 'r')
            self._geom_info = file_handle.read()
            file_handle.close()
            # load free space (always material 0)
            mat_fs = self._mat_free_space.search(self._geom_info)
            self._materials.append(XFMaterial())
            self._materials[0].name = mat_fs.group(1)
            self._materials[0].conductivity = float(mat_fs.group(3))
            self._materials[0].epsilon_r = float(mat_fs.group(4))
            self._materials[0].density = float(mat_fs.group(5))

            # load PEC (always material 1)
            mat_pec = self._mat_pec.search(self._geom_info)
            self._materials.append(XFMaterial())
            self._materials[1].name = mat_pec.group(1)

            # load normal electric values
            mat1 = self._mat_norm_electric.findall(self._geom_info)

            for mat_index in range(len(mat1)):
                self._materials.append(XFMaterial())
                self._materials[-1].name = mat1[mat_index][self.NAME]
                self._materials[-1].conductivity = float(mat1[mat_index][self.CONDUCTIVITY])
                self._materials[-1].density = float(mat1[mat_index][self.DENSITY])
                self._materials[-1].epsilon_r = float(mat1[mat_index][self.PERMITTIVITY])
                self._materials[-1].tissue = int(mat1[mat_index][self.TISSUE])
        else:
            print("Could not find file: ", self._geometry_input_file_path)

        return self._materials

    def _load_grid_data(self):
        """Load grid data from material.input"""
        if os.path.exists(self._geometry_input_file_path):
            file_handle = open(self._geometry_input_file_path, 'r')
            self._geom_info = file_handle.read()
            file_handle.close()
            # load grid information
            grid_def1 = self._grid_definition.search(self._geom_info)
            self.grid_data.origin = [float(grid_def1.group(1)), \
                                     float(grid_def1.group(2)), \
                                     float(grid_def1.group(3))]
            self.grid_data.num_x_cells = int(grid_def1.group(4))
            self.grid_data.num_y_cells = int(grid_def1.group(5))
            self.grid_data.num_z_cells = int(grid_def1.group(6))

            ind_begin_delx = self._begin_delx.search(self._geom_info).span()[1]
            ind_end_delx = self._end_delx.search(self._geom_info).span()[0]
            ind_begin_dely = self._begin_dely.search(self._geom_info).span()[1]
            ind_end_dely = self._end_dely.search(self._geom_info).span()[0]
            ind_begin_delz = self._begin_delz.search(self._geom_info).span()[1]
            ind_end_delz = self._end_delz.search(self._geom_info).span()[0]
            self.grid_data.x_deltas = self._grid_delta.findall( \
                                  self._geom_info[ind_begin_delx:ind_end_delx])
            self.grid_data.y_deltas = self._grid_delta.findall( \
                                  self._geom_info[ind_begin_dely:ind_end_dely])
            self.grid_data.z_deltas = self._grid_delta.findall( \
                                  self._geom_info[ind_begin_delz:ind_end_delz])
        else:
            print("Could not find file: ", self._geometry_input_file_path)

