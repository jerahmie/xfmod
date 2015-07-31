import sys, re

class GeometryXF:
    """A class to hold coil geometry info."""
    _MAT_FREESPACE_PATTERN = r'^begin_<electricfreespace> ' + \
                                '(ElectricFreeSpace)\n' + \
                                'material_number (\d+)\n' + \
                                'conductivity ([\d\-eE.]*)\n' + \
                                'permittivity ([\d\-eE.]*)\n' + \
                                'density ([\d\-eE.]*)\n' + \
                                'water_ratio ([\d\-eE.]*)\n' + \
                                'end_<electricfreespace>'
    _MAT_PEC_PATTERN = r'^begin_<electricperfectconductor> ' + \
                          '(ElectricPerfectConductor)\n' + \
                          'material_number (\d+)\n' + \
                          'end_<electricperfectconductor>'
    _MAT_NORMALELECTRIC_PATTERN = r'^begin_<normal_electric>\s*' + \
                                     '([\w\s\d\-\(\)]+)\s*\n' + \
                                     'material_number (\d+)\n' + \
                                     'conductivity ([\d\-eE.]*)\n'+ \
                                     'uncorrected_conductivity ' + \
                                     '([\d\-eE.]*)\n' + \
                                     'permittivity ([\d\-eE.]*)\n' + \
                                     '(effectiveConductivity\s*' +\
                                     '[\d\-eE.]*\n)?' + \
                                     '(effectiveUncorrectedConductivity\s*' + \
                                     '[\d\-eE.]*\n)?' + \
                                     '(effectiveRelativePermittivity\s*' + \
                                     '[\d\-eE.]*\n)?' + \
                                     'density ([\d\-eE.]*)\n' + \
                                     'water_ratio ([\d\-eE.]*)\nbegin_' + \
                                     '<TemperatureRiseMaterial' + \
                                     'Parameters>\s*\n' + \
                                     'heat_capacity ([\d\-eE.]*)\n' + \
                                     'thermal_conductivity ([\d\-eE.]*)\n' + \
                                     'perfusion_rate ([\d\-eE.]*)\n' + \
                                     'metabolic_heat ([\d\-eE.]*)\n' + \
                                     'tissue (\d+)\nend_' + \
                                     '<TemperatureRiseMaterialParameters>' + \
                                     '\s*\nend_<normal_electric>'
                                  
    fileHandle = None

    def __init__(self, fileHandle):
        # compile patterns
        self._matFreeSpace = re.compile(self._MAT_FREESPACE_PATTERN, \
                                              re.MULTILINE)
        self._matPEC = re.compile(self._MAT_PEC_PATTERN, re.MULTILINE)
        self._matNormElectric = re.compile(self._MAT_NORMALELECTRIC_PATTERN, \
                                            re.MULTILINE)

        self.fileHandle = fileHandle
        self.loadMaterials()

    def loadMaterials(self):
        geomInfo = self.fileHandle.read()
        #m = self._matFreeSpace.findall(geomInfo)
        #print(m)
        #m = self._matPEC.findall(geomInfo)
        #print(m)
        m = self._matNormElectric.findall(geomInfo)
        print(m[0][0])
        print(m[1][0])
        print(m[2][0])
                
        
def main(argv):
    f = open(argv,"r")
    xfGeom = GeometryXF(f);
    f.close()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print('Usage: xf_geometry.py <inputfile>')
        print(sys.argv)
