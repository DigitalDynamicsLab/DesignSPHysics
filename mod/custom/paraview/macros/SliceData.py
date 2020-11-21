from paraview.simple import *

parent = GetActiveSource()
parentDisplay = GetDisplayProperties(parent, view=GetActiveView())

parentDisplay.Opacity = 0.1

slice_00 = Slice(Input=parent)
slice_00.SliceType = 'Plane'
RenameSource('Slice',slice_00)

sliceAvg_00 = ProgrammableFilter(Input=FindSource('Slice'))
sliceAvg_00.PythonPath=["'C:/Users/penzo/AppData/Roaming/FreeCAD/Mod/DesignSPHysics/mod/paraview/macros'"]
sliceAvg_00.OutputDataSetType = "vtkPolyData"    
sliceAvg_00.Script = "from pv_slice import slice_data\nslicedata = slice_data(self)\nself.GetOutput(0).DeepCopy(slicedata)\n"    
RenameSource('SliceData',sliceAvg_00)

sliceAvg_00Display = Show(sliceAvg_00, GetActiveView(), 'GeometryRepresentation')
sliceAvg_00Display.Representation = 'Surface'

avgCoordNumLUT = GetColorTransferFunction('AvgCoordNum')
avgCoordNumLUTColorBar = GetScalarBar(avgCoordNumLUT, GetActiveView())
avgCoordNumLUTColorBar.Title = 'AvgCoordNum'
avgCoordNumLUTColorBar.ComponentTitle = ''
avgCoordNumLUTColorBar.Visibility = 1

sliceAvg_00Display.SetScalarBarVisibility(GetActiveView(), True)

ColorBy(sliceAvg_00Display, ('POINTS', 'AvgCoordNum'))

sliceDataTrack = GetAnimationTrack('Origin', index=0, proxy=slice_00.SliceType)

AFrame = CompositeKeyFrame()
AFrame.KeyValues = [0.00719695]

BFrame = CompositeKeyFrame()
BFrame.KeyTime = 1.0
BFrame.KeyValues = [0.772145]

sliceDataTrack.KeyFrames = [AFrame, BFrame]

animationScene1 = GetAnimationScene()
animationScene1.NumberOfFrames = 500