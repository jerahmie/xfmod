"""
A python class to represent voxel data.
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import sys, os.path, ntpath
import csv
import numpy as np
import vtk

class VoxelData(object):
    """
    A class to store voxel data.  A valid voxel data object will be
    initialized with a voxelInfo object.
    """
    def __init__(self, voxelInfo):
        self._voxelInfo = voxelInfo
        # Active voxel data for display and manipulation
        self._voxelData = None
        # Original voxel data for revert
        self._voxelDataOriginal = None
        self._fileName = None
        self._fileHandle = None

    def loadVoxelData(self, fileName):
        """Loads voxel data into numpy array."""
        if os.path.isfile(fileName):
            self._fileName = fileName
        else:
            raise Exception("File name: ", fileName, " does not exist.")
        try:
            #self._fileHandle = open(self._fileName, 'rb')
            self._voxelDataOriginal = np.fromfile(fileName, count=(self._voxelInfo.nx*self._voxelInfo.ny*self._voxelInfo.nz),dtype=np.uint8).reshape((self._voxelInfo.nz, self._voxelInfo.ny, self._voxelInfo.nx))
#            self._voxelDataOriginal = np.fromfile(fileName, count=(self._voxelInfo.nx*self._voxelInfo.ny*self._voxelInfo.nz),dtype=np.uint8)            
            self._voxelData = np.copy(self._voxelDataOriginal)
            print(np.amax(self._voxelData))

            print(self._voxelData.shape)
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))

    def _printVTKInteractorInstructions(self):
        print("\n\nKeyboard bindings (upper or lower case):")
        print("\tj - joystick like mouse interactions")
        print("\tt - trackball like mouse interactions")
        print("\to - object/ actor interaction")
        print("\tc - camera interaction")
        print("\tr - reset camera view")
        print("\tw - turn all actors wireframe")
        print("\ts - turn all actors surface")
        print("\tu - execute user defined function")
        print("\tp - pick actor under mouse pointer (if pickable)")
        print("\t3 - toggle in/out of 3D mode (if supported by renderer)")
        print("\te - exit")
        print("\tq - exit\n")

    def plotVoxelData(self):
        """Plot voxel data in a python vtk window"""
        print("Plotting voxel data....")
        # Following this example:
        #  http://www.vtk.org/Wiki/VTK/Examples/Python/vtkWithNumpy
        dataString = self._voxelData.tostring()

        # Import data
        dataImporter = vtk.vtkImageImport()
        dataImporter.CopyImportVoidPointer(dataString, len(dataString))
        dataImporter.SetDataScalarTypeToUnsignedChar()
        dataImporter.SetNumberOfScalarComponents(1)
        dataImporter.SetDataExtent( 0, self._voxelData.shape[2]-1,
                                    0, self._voxelData.shape[1]-1,
                                    0, self._voxelData.shape[0]-1)
        dataImporter.SetWholeExtent(0, self._voxelData.shape[2]-1,
                                    0, self._voxelData.shape[1]-1,
                                    0, self._voxelData.shape[0]-1)

        # Set alpha channel (transparency)
        alphaChannelFunc = vtk.vtkPiecewiseFunction()
        alphaChannelFunc.AddPoint(0, 0.0)
        alphaChannelFunc.AddPoint(1, 0.1)
        alphaChannelFunc.AddPoint(5, 0.1)        
        alphaChannelFunc.AddPoint(6, 1.0)
        alphaChannelFunc.AddPoint(7, 0.1)        
        alphaChannelFunc.AddPoint(77, 0.1)
        
        # Set colors
        funcColor = vtk.vtkColorTransferFunction()

        for idx in range(0, self._voxelInfo.numMaterials):
            funcColor.AddRGBPoint(idx,
                                  self._voxelInfo.material(idx)[2],
                                  self._voxelInfo.material(idx)[3],
                                  self._voxelInfo.material(idx)[4])

        # Set volume properties
        volumeProperty = vtk.vtkVolumeProperty()
        volumeProperty.SetColor(funcColor)
        volumeProperty.SetScalarOpacity(alphaChannelFunc)
        # propVolume.ShadeOff()

        # Set ray tracing volume rendering
        compositeFunction = vtk.vtkVolumeRayCastCompositeFunction()

        volumeMapper = vtk.vtkVolumeRayCastMapper()
        volumeMapper.SetVolumeRayCastFunction(compositeFunction)
        volumeMapper.SetInputConnection(dataImporter.GetOutputPort())

        volume = vtk.vtkVolume()
        volume.SetMapper(volumeMapper)
        volume.SetProperty(volumeProperty)

        # create a camera
        camera = vtk.vtkCamera()
        camera.SetPosition(0,10,0)
        camera.SetFocalPoint(0,0,0)

        # Create the graphics structure. The renderer renders into the render
        # window. The render window interactor captures mouse events and will
        # perform appropriate camera or actor manipulation depending on the
        # nature of the events.
        renderer = vtk.vtkRenderer()
        renderWin = vtk.vtkRenderWindow()
        renderWin.AddRenderer(renderer)
        iren = vtk.vtkRenderWindowInteractor()
        iren.SetRenderWindow(renderWin)
    
        # add volume to renderer
        renderer.AddVolume(volume)

        # set background and size
        renderer.SetBackground(0.1, 0.2, 0.4)
        renderer.SetActiveCamera(camera)
        renderer.ResetCamera()
        renderWin.SetSize(400, 300)

        # This allows the interactor to initalize itself. It has to be
        # called before an event loop.
        iren.Initialize()
        self._printVTKInteractorInstructions()

        renderWin.Render()
        iren.Start()

        
    def voxelDataSubRegion(self, rangeX, rangeY, rangeZ):
        """
        Set set the voxelRegion as a subregion of the original data.

        Keyword arguments:
        rangeX -- 
        rangeY --
        rangeZ -- 
        """
        print("Obtain voxel data subregion:")
        print(self._voxelData.shape)
        if (len(rangeX) == 2) and (len(rangeY) ==2) and (len(rangeZ) == 2):
            self._voxelData = np.copy(
                self._voxelDataOriginal[rangeZ[0]:rangeZ[1],
                                        rangeY[0]:rangeY[1],
                                        rangeX[0]:rangeX[1]])
        else:
            print("Range values were not correct")
        print(self._voxelData.shape)

    def saveVoxelData(self, fileName):
        """
        Save the active voxelData array to a file.
        """
        self._voxelData.tofile(fileName)

    def saveVoxelInfo(self, fileName):
        """
        Save material data to file
        """
        f = open(fileName, 'w')
        # write material info: [Material Index] [R] [G] [B] [Material Name]
        for idx in range(1,self._voxelInfo.numMaterials):
            f.write(str(idx) + '\t' + str(self._voxelInfo.material(idx)[2]) +
                    '\t' + str(self._voxelInfo.material(idx)[3]) +
                    '\t' + str(self._voxelInfo.material(idx)[4]) +
                    '\t' + self._voxelInfo.material(idx)[1] +'\n')

        # write grid extent
        f.write('\nGrid extent (number of cells)\n')
        f.write('nx\t' + str(self._voxelData.shape[2]) + '\n')
        f.write('ny\t' + str(self._voxelData.shape[1]) + '\n')
        f.write('nz\t' + str(self._voxelData.shape[0]) + '\n')

        # write spatial steps (resolution)
        f.write('\nSpatial steps [m]\n')
        f.write('dx\t' + str(self._voxelInfo.dx) + '\n')
        f.write('dy\t' + str(self._voxelInfo.dy) + '\n')
        f.write('dz\t' + str(self._voxelInfo.dz) + '\n')
        f.close()
