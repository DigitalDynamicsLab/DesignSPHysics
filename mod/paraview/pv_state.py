# state file generated using paraview version 5.8.0

# ----------------------------------------------------------------
# setup views used in the visualization
# ----------------------------------------------------------------

import os
import sys
print(os.path.abspath(__file__))

import pippo

from paraview.simple import *

paraview.simple._DisableFirstRenderCameraReset()

# Create a new 'Line Chart View'
lineChartView1 = CreateView('XYChartView')
lineChartView1.ViewSize = [796, 805]
lineChartView1.LegendPosition = [621, 729]
lineChartView1.LeftAxisTitle = '% Mixing Index'
lineChartView1.LeftAxisRangeMaximum = 40.0
lineChartView1.BottomAxisTitle = 'Timestep'
lineChartView1.BottomAxisRangeMaximum = 26.0
lineChartView1.RightAxisRangeMaximum = 6.66
lineChartView1.TopAxisRangeMaximum = 6.66

# get the material library
materialLibrary1 = GetMaterialLibrary()

# Create a new 'Render View'
renderView1 = CreateView('RenderView')
renderView1.ViewSize = [796, 805]
renderView1.AxesGrid = 'GridAxes3DActor'
renderView1.CenterOfRotation = [0.390000001527369, 0.0, 0.0]
renderView1.StereoType = 'Crystal Eyes'
renderView1.CameraPosition = [0.390000001527369, -2.246144805107603, 0.0]
renderView1.CameraFocalPoint = [0.390000001527369, 0.0, 0.0]
renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraFocalDisk = 1.0
renderView1.CameraParallelScale = 0.5817784886558562
renderView1.BackEnd = 'OSPRay raycaster'
renderView1.OSPRayMaterialLibrary = materialLibrary1

SetActiveView(None)

# ----------------------------------------------------------------
# setup view layouts
# ----------------------------------------------------------------

# create new layout object 'Layout #1'
layout1 = CreateLayout(name='Layout #1')
layout1.SplitHorizontal(0, 0.500000)
layout1.AssignView(1, renderView1)
layout1.AssignView(2, lineChartView1)

# ----------------------------------------------------------------
# restore active view
SetActiveView(renderView1)
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

# create a new 'CSV Reader'
mixingIndex_Variancecsv = CSVReader(FileName=['C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\PartFluid\\MixingIndex_Variance.csv'])

# create a new 'Legacy VTK Reader'
partFluid_00 = LegacyVTKReader(FileNames=['C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\PartFluid\\PartFluid_0000.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\PartFluid\\PartFluid_0001.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\PartFluid\\PartFluid_0002.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\PartFluid\\PartFluid_0003.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\PartFluid\\PartFluid_0004.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\PartFluid\\PartFluid_0005.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\PartFluid\\PartFluid_0006.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\PartFluid\\PartFluid_0007.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\PartFluid\\PartFluid_0008.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\PartFluid\\PartFluid_0009.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\PartFluid\\PartFluid_0010.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\PartFluid\\PartFluid_0011.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\PartFluid\\PartFluid_0012.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\PartFluid\\PartFluid_0013.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\PartFluid\\PartFluid_0014.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\PartFluid\\PartFluid_0015.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\PartFluid\\PartFluid_0016.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\PartFluid\\PartFluid_0017.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\PartFluid\\PartFluid_0018.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\PartFluid\\PartFluid_0019.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\PartFluid\\PartFluid_0020.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\PartFluid\\PartFluid_0021.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\PartFluid\\PartFluid_0022.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\PartFluid\\PartFluid_0023.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\PartFluid\\PartFluid_0024.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\PartFluid\\PartFluid_0025.vtk'])

# create a new 'Legacy VTK Reader'
boundaryMoving_00 = LegacyVTKReader(FileNames=['C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\BoundaryMoving\\BoundaryMoving_0000.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\BoundaryMoving\\BoundaryMoving_0001.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\BoundaryMoving\\BoundaryMoving_0002.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\BoundaryMoving\\BoundaryMoving_0003.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\BoundaryMoving\\BoundaryMoving_0004.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\BoundaryMoving\\BoundaryMoving_0005.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\BoundaryMoving\\BoundaryMoving_0006.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\BoundaryMoving\\BoundaryMoving_0007.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\BoundaryMoving\\BoundaryMoving_0008.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\BoundaryMoving\\BoundaryMoving_0009.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\BoundaryMoving\\BoundaryMoving_0010.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\BoundaryMoving\\BoundaryMoving_0011.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\BoundaryMoving\\BoundaryMoving_0012.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\BoundaryMoving\\BoundaryMoving_0013.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\BoundaryMoving\\BoundaryMoving_0014.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\BoundaryMoving\\BoundaryMoving_0015.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\BoundaryMoving\\BoundaryMoving_0016.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\BoundaryMoving\\BoundaryMoving_0017.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\BoundaryMoving\\BoundaryMoving_0018.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\BoundaryMoving\\BoundaryMoving_0019.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\BoundaryMoving\\BoundaryMoving_0020.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\BoundaryMoving\\BoundaryMoving_0021.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\BoundaryMoving\\BoundaryMoving_0022.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\BoundaryMoving\\BoundaryMoving_0023.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\BoundaryMoving\\BoundaryMoving_0024.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\BoundaryMoving\\BoundaryMoving_0025.vtk'])

# create a new 'CSV Reader'
mixingIndex_Averagecsv = CSVReader(FileName=['C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\PartFluid\\MixingIndex_Average.csv'])

# create a new 'Legacy VTK Reader'
isosurface_00 = LegacyVTKReader(FileNames=['C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\IsoSurface\\Isosurface_0000.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\IsoSurface\\Isosurface_0001.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\IsoSurface\\Isosurface_0002.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\IsoSurface\\Isosurface_0003.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\IsoSurface\\Isosurface_0004.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\IsoSurface\\Isosurface_0005.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\IsoSurface\\Isosurface_0006.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\IsoSurface\\Isosurface_0007.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\IsoSurface\\Isosurface_0008.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\IsoSurface\\Isosurface_0009.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\IsoSurface\\Isosurface_0010.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\IsoSurface\\Isosurface_0011.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\IsoSurface\\Isosurface_0012.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\IsoSurface\\Isosurface_0013.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\IsoSurface\\Isosurface_0014.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\IsoSurface\\Isosurface_0015.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\IsoSurface\\Isosurface_0016.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\IsoSurface\\Isosurface_0017.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\IsoSurface\\Isosurface_0018.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\IsoSurface\\Isosurface_0019.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\IsoSurface\\Isosurface_0020.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\IsoSurface\\Isosurface_0021.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\IsoSurface\\Isosurface_0022.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\IsoSurface\\Isosurface_0023.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\IsoSurface\\Isosurface_0024.vtk', 'C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\IsoSurface\\Isosurface_0025.vtk'])

# create a new 'Legacy VTK Reader'
boundaryvtk = LegacyVTKReader(FileNames=['C:\\Users\\penzo\\Documents\\DSPHProject\\RheologyEstimation\\rhe_est\\rhe_est_out\\Boundary.vtk'])

# ----------------------------------------------------------------
# setup the visualization in view 'lineChartView1'
# ----------------------------------------------------------------

# show data from mixingIndex_Variancecsv
mixingIndex_VariancecsvDisplay = Show(mixingIndex_Variancecsv, lineChartView1, 'XYChartRepresentation')

# trace defaults for the display properties.
mixingIndex_VariancecsvDisplay.CompositeDataSetIndex = [0]
mixingIndex_VariancecsvDisplay.AttributeType = 'Row Data'
mixingIndex_VariancecsvDisplay.UseIndexForXAxis = 0
mixingIndex_VariancecsvDisplay.XArrayName = 'Timestep'
mixingIndex_VariancecsvDisplay.SeriesVisibility = ['Kramer', 'Lacey']
mixingIndex_VariancecsvDisplay.SeriesLabel = ['Kramer', 'Kramer', 'Lacey', 'Lacey', 'Timestep', 'Timestep']
mixingIndex_VariancecsvDisplay.SeriesColor = ['Kramer', '0', '0', '0', 'Lacey', '0.89', '0.1', '0.11', 'Timestep', '0.22', '0.49', '0.72']
mixingIndex_VariancecsvDisplay.SeriesPlotCorner = ['Kramer', '0', 'Lacey', '0', 'Timestep', '0']
mixingIndex_VariancecsvDisplay.SeriesLabelPrefix = ''
mixingIndex_VariancecsvDisplay.SeriesLineStyle = ['Kramer', '1', 'Lacey', '1', 'Timestep', '1']
mixingIndex_VariancecsvDisplay.SeriesLineThickness = ['Kramer', '2', 'Lacey', '2', 'Timestep', '2']
mixingIndex_VariancecsvDisplay.SeriesMarkerStyle = ['Kramer', '0', 'Lacey', '0', 'Timestep', '0']
mixingIndex_VariancecsvDisplay.SeriesMarkerSize = ['Kramer', '4', 'Lacey', '4', 'Timestep', '4']

# show data from mixingIndex_Averagecsv
mixingIndex_AveragecsvDisplay = Show(mixingIndex_Averagecsv, lineChartView1, 'XYChartRepresentation')

# trace defaults for the display properties.
mixingIndex_AveragecsvDisplay.CompositeDataSetIndex = [0]
mixingIndex_AveragecsvDisplay.AttributeType = 'Row Data'
mixingIndex_AveragecsvDisplay.UseIndexForXAxis = 0
mixingIndex_AveragecsvDisplay.XArrayName = 'Timestep'
mixingIndex_AveragecsvDisplay.SeriesVisibility = ['AverageMixingIndex']
mixingIndex_AveragecsvDisplay.SeriesLabel = ['AverageMixingIndex', 'AverageMixingIndex', 'Timestep', 'Timestep']
mixingIndex_AveragecsvDisplay.SeriesColor = ['AverageMixingIndex', '0', '0.666667', '0', 'Timestep', '0.889998', '0.100008', '0.110002']
mixingIndex_AveragecsvDisplay.SeriesPlotCorner = ['AverageMixingIndex', '0', 'Timestep', '0']
mixingIndex_AveragecsvDisplay.SeriesLabelPrefix = ''
mixingIndex_AveragecsvDisplay.SeriesLineStyle = ['AverageMixingIndex', '1', 'Timestep', '1']
mixingIndex_AveragecsvDisplay.SeriesLineThickness = ['AverageMixingIndex', '2', 'Timestep', '2']
mixingIndex_AveragecsvDisplay.SeriesMarkerStyle = ['AverageMixingIndex', '0', 'Timestep', '0']
mixingIndex_AveragecsvDisplay.SeriesMarkerSize = ['AverageMixingIndex', '4', 'Timestep', '4']

# ----------------------------------------------------------------
# setup the visualization in view 'renderView1'
# ----------------------------------------------------------------

# show data from isosurface_00
isosurface_00Display = Show(isosurface_00, renderView1, 'GeometryRepresentation')

# get color transfer function/color map for 'TracCnt'
tracCntLUT = GetColorTransferFunction('TracCnt')
tracCntLUT.ScalarRangeInitialized = 1.0

# trace defaults for the display properties.
isosurface_00Display.Representation = 'Surface'
isosurface_00Display.ColorArrayName = ['POINTS', 'TracCnt']
isosurface_00Display.LookupTable = tracCntLUT
isosurface_00Display.OSPRayScaleArray = 'TracCnt'
isosurface_00Display.OSPRayScaleFunction = 'PiecewiseFunction'
isosurface_00Display.SelectOrientationVectors = 'None'
isosurface_00Display.ScaleFactor = 0.07600256130099298
isosurface_00Display.SelectScaleArray = 'TracCnt'
isosurface_00Display.GlyphType = 'Arrow'
isosurface_00Display.GlyphTableIndexArray = 'TracCnt'
isosurface_00Display.GaussianRadius = 0.0038001280650496482
isosurface_00Display.SetScaleArray = ['POINTS', 'TracCnt']
isosurface_00Display.ScaleTransferFunction = 'PiecewiseFunction'
isosurface_00Display.OpacityArray = ['POINTS', 'TracCnt']
isosurface_00Display.OpacityTransferFunction = 'PiecewiseFunction'
isosurface_00Display.DataAxesGrid = 'GridAxesRepresentation'
isosurface_00Display.PolarAxes = 'PolarAxesRepresentation'

# show data from boundaryMoving_00
boundaryMoving_00Display = Show(boundaryMoving_00, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
boundaryMoving_00Display.Representation = 'Surface'
boundaryMoving_00Display.ColorArrayName = ['POINTS', '']
boundaryMoving_00Display.OSPRayScaleFunction = 'PiecewiseFunction'
boundaryMoving_00Display.SelectOrientationVectors = 'None'
boundaryMoving_00Display.ScaleFactor = 0.07738955058157444
boundaryMoving_00Display.SelectScaleArray = 'Mk'
boundaryMoving_00Display.GlyphType = 'Arrow'
boundaryMoving_00Display.GlyphTableIndexArray = 'Mk'
boundaryMoving_00Display.GaussianRadius = 0.003869477529078722
boundaryMoving_00Display.SetScaleArray = [None, '']
boundaryMoving_00Display.ScaleTransferFunction = 'PiecewiseFunction'
boundaryMoving_00Display.OpacityArray = [None, '']
boundaryMoving_00Display.OpacityTransferFunction = 'PiecewiseFunction'
boundaryMoving_00Display.DataAxesGrid = 'GridAxesRepresentation'
boundaryMoving_00Display.PolarAxes = 'PolarAxesRepresentation'

# show data from boundaryvtk
boundaryvtkDisplay = Show(boundaryvtk, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
boundaryvtkDisplay.Representation = 'Surface'
boundaryvtkDisplay.ColorArrayName = ['POINTS', '']
boundaryvtkDisplay.Opacity = 0.1
boundaryvtkDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
boundaryvtkDisplay.SelectOrientationVectors = 'None'
boundaryvtkDisplay.ScaleFactor = 0.08400000017136336
boundaryvtkDisplay.SelectScaleArray = 'Mk'
boundaryvtkDisplay.GlyphType = 'Arrow'
boundaryvtkDisplay.GlyphTableIndexArray = 'Mk'
boundaryvtkDisplay.GaussianRadius = 0.004200000008568168
boundaryvtkDisplay.SetScaleArray = [None, '']
boundaryvtkDisplay.ScaleTransferFunction = 'PiecewiseFunction'
boundaryvtkDisplay.OpacityArray = [None, '']
boundaryvtkDisplay.OpacityTransferFunction = 'PiecewiseFunction'
boundaryvtkDisplay.DataAxesGrid = 'GridAxesRepresentation'
boundaryvtkDisplay.PolarAxes = 'PolarAxesRepresentation'

# setup the color legend parameters for each legend in this view

# get color legend/bar for tracCntLUT in view renderView1
tracCntLUTColorBar = GetScalarBar(tracCntLUT, renderView1)
tracCntLUTColorBar.Title = 'TracCnt'
tracCntLUTColorBar.ComponentTitle = ''

# set color bar visibility
tracCntLUTColorBar.Visibility = 1

# show color legend
isosurface_00Display.SetScalarBarVisibility(renderView1, True)

# ----------------------------------------------------------------
# setup color maps and opacity mapes used in the visualization
# note: the Get..() functions create a new object, if needed
# ----------------------------------------------------------------

# get opacity transfer function/opacity map for 'TracCnt'
tracCntPWF = GetOpacityTransferFunction('TracCnt')
tracCntPWF.ScalarRangeInitialized = 1

# ----------------------------------------------------------------
# finally, restore active source
SetActiveSource(isosurface_00)
# ----------------------------------------------------------------