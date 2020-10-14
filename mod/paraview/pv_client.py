#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Paraview client"""

import os

import pickle

from socket import *

from paraview.simple import *
 
class ParaviewState:
    
    def __init__(self,pv_params):
    
        case = pv_params["outdir"]
        
        self.clientMessage = ''
        
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
        layout1 = CreateLayout(name=pv_params["name"])
        layout1.SplitHorizontal(0, 0.500000)
        layout1.AssignView(1, renderView1)
        layout1.AssignView(2, lineChartView1)
        
        # ----------------------------------------------------------------
        # restore active view
        SetActiveView(renderView1)
        # ----------------------------------------------------------------
              
        # ----------------------------------------------------------------
        # setup the visualization in view 'renderView1'
        # ----------------------------------------------------------------
        
        if os.path.isfile(case+"/{}.vtk".format(pv_params["boundaryfixed"])):
            # create a new 'Legacy VTK Reader'
            boundaryvtk = LegacyVTKReader(FileNames=case+"/{}.vtk".format(pv_params["boundaryfixed"]))
            
            if boundaryvtk is not None:
                #rename source
                RenameSource('BoundaryFixed',boundaryvtk)
                
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
            else:
                self.clientMessage += '     Fixed boundary *.vtk-'
        else:
            self.clientMessage += '     Fixed boundary *.vtk-'
            
        if os.path.isdir(case+"/{}".format(pv_params["boundarymoving"])):
            # create a new 'Legacy VTK Reader'
            boundaryMoving_00 = self.load_vtk(case+"/{}".format(pv_params["boundarymoving"]))
            
            if boundaryMoving_00 is not None:
                #rename source
                RenameSource('BoundaryMoving',boundaryMoving_00)
                
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
            else:
                self.clientMessage += '     Moving boundary *.vtk-'
        else:
            self.clientMessage += '     Moving boundary *.vtk-'
        
        if os.path.isdir(case+"/{}".format(pv_params["partfluid"])):          
            # create a new 'Legacy VTK Reader'
            partFluid_00 = self.load_vtk(case+"/{}".format(pv_params["partfluid"]))
            
            if partFluid_00 is not None:
                #rename source
                RenameSource('PartFluid',partFluid_00)
                
                #show data from partFluid
                partFluidDisplay = Show(partFluid_00, renderView1, 'GeometryRepresentation')
                
                # get color transfer function/color map for 'Idp'
                idpLUT = GetColorTransferFunction('Idp')
                idpLUT.RGBPoints = [11373.0, 0.231373, 0.298039, 0.752941, 16806.5, 0.865003, 0.865003, 0.865003, 22240.0, 0.705882, 0.0156863, 0.14902]
                idpLUT.ScalarRangeInitialized = 1.0
                
                # trace defaults for the display properties.
                partFluidDisplay.Representation = 'Points'
                partFluidDisplay.ColorArrayName = ['POINTS', 'Idp']
                partFluidDisplay.LookupTable = idpLUT
                partFluidDisplay.PointSize = 7.0
                partFluidDisplay.RenderPointsAsSpheres = 1
                partFluidDisplay.OSPRayScaleArray = 'Idp'
                partFluidDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
                partFluidDisplay.SelectOrientationVectors = 'Idp'
                partFluidDisplay.ScaleFactor = 0.07399999909102917
                partFluidDisplay.SelectScaleArray = 'Idp'
                partFluidDisplay.GlyphType = 'Arrow'
                partFluidDisplay.GlyphTableIndexArray = 'Idp'
                partFluidDisplay.GaussianRadius = 0.0036999999545514585
                partFluidDisplay.SetScaleArray = ['POINTS', 'Idp']
                partFluidDisplay.ScaleTransferFunction = 'PiecewiseFunction'
                partFluidDisplay.OpacityArray = ['POINTS', 'Idp']
                partFluidDisplay.OpacityTransferFunction = 'PiecewiseFunction'
                partFluidDisplay.DataAxesGrid = 'GridAxesRepresentation'
                partFluidDisplay.PolarAxes = 'PolarAxesRepresentation'
                
                # init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
                partFluidDisplay.ScaleTransferFunction.Points = [11373.0, 0.0, 0.5, 0.0, 22240.0, 1.0, 0.5, 0.0]
                
                # init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
                partFluidDisplay.OpacityTransferFunction.Points = [11373.0, 0.0, 0.5, 0.0, 22240.0, 1.0, 0.5, 0.0]
                
                # setup the color legend parameters for each legend in this view
                
                # get color legend/bar for idpLUT in view renderView1
                idpLUTColorBar = GetScalarBar(idpLUT, renderView1)
                idpLUTColorBar.WindowLocation = 'UpperRightCorner'
                idpLUTColorBar.Title = 'Idp'
                idpLUTColorBar.ComponentTitle = ''
                
                # set color bar visibility
                idpLUTColorBar.Visibility = 0
            else:
                self.clientMessage += '     Fluid particles *.vtk-'
        else:
            self.clientMessage += '     Fluid particles *.vtk-'
        
        if os.path.isdir(case+"/{}".format(pv_params["isosurface"])):
            
            # create a new 'Legacy VTK Reader'
            isosurface_00 = self.load_vtk(case+"/{}".format(pv_params["isosurface"]))
            
            if isosurface_00 is not None:
                # hide data in view
                Hide(partFluid_00, renderView1)
                
                #rename source
                RenameSource('IsoSurface',isosurface_00)
                
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
            else:
                self.clientMessage += '     IsoSurface *.vtk-'
        else:
            self.clientMessage += '     IsoSurface *.vtk-'
                
        # ----------------------------------------------------------------
        # setup the visualization in view 'lineChartView1'
        # ----------------------------------------------------------------
        
        if os.path.isfile(case+'/PartFluid/MixingIndex_Average.csv'):
            # create a new 'CSV Reader'
            mixingIndex_Averagecsv = CSVReader(FileName=case+'/PartFluid/MixingIndex_Average.csv')
            
            #rename source
            RenameSource('AverageMixingIndex',mixingIndex_Averagecsv) 
            
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
        else:
            self.clientMessage += '     Average mixing index *.csv-'
            
        if os.path.isfile(case+'/PartFluid/MixingIndex_Variance.csv'):
            # create a new 'CSV Reader'
            mixingIndex_Variancecsv = CSVReader(FileName=case+'/PartFluid/MixingIndex_Variance.csv')
            
            #rename source
            RenameSource('VarianceMixingIndex',mixingIndex_Variancecsv)  
            
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
        else:
            self.clientMessage += '     Variance mixing index *.csv-'
            
    def load_vtk(self,dirin):   
        vtk_name = dirin.split('/')[-1]
        vtk_files = [f for f in os.listdir(dirin) if os.path.isfile(os.path.join(dirin,f))]
        vtk_files = [dirin + '\\' + f for f in vtk_files if (f.find(vtk_name)>=0 and f.find('vtk') >= 0)]
        if len(vtk_files) > 0:
            return LegacyVTKReader(FileNames=vtk_files)
        else:
            return None

serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.sendto(("Client Ready").encode(), (serverName, serverPort))

serverParams, serverAddress = clientSocket.recvfrom(2048)

pv_params = pickle.loads(serverParams)

pv_state = ParaviewState(pv_params)
clientSocket.sendto(pv_state.clientMessage.encode(), (serverName, serverPort))
clientSocket.close()
    
