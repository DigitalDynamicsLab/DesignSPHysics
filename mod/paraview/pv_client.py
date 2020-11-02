#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Paraview client"""

import sys
        
import os

import pickle

from socket import *

from paraview.simple import *
        
class MVolume:
    
    def __init__(self):
        fluid = ProgrammableFilter.GetInputDataObject(0,0)
        iso = ProgrammableFilter.GetInputDataObject(0,1)

        fluidName=''
        fluidInfo = fluid.GetFieldData().GetArray("FileInfo")
        for n in range(0,fluidInfo.GetNumberOfValues()):
            fluidName+=str(fluidInfo.GetVariantValue(n))
         
        isoName=''
        isoInfo = iso.GetFieldData().GetArray("FileInfo")
        for n in range(0,isoInfo.GetNumberOfValues()):
            isoName+=str(isoInfo.GetVariantValue(n))

        print(fluidName)
        print(isoName)
                
class ParaviewState:
    
    def __init__(self,pv_params):
    
        case = pv_params["outdir"]
        
        self.clientMessage = ''
                
        partFluid_00 = self.load_vtk(case+"/{}".format(pv_params["partfluid"]))
        RenameSource('PartFluid',partFluid_00)
        
        isosurface_00 = self.load_vtk(case+"/{}".format(pv_params["isosurface"]))
        RenameSource('IsoSurface',isosurface_00)     
        
        boundaryvtk = LegacyVTKReader(FileNames=case+"/{}.vtk".format(pv_params["boundaryfixed"]))
        RenameSource('BoundaryFixed',boundaryvtk)
        
        boundaryMoving_00 = self.load_vtk(case+"/{}".format(pv_params["boundarymoving"]))
        RenameSource('BoundaryMoving',boundaryMoving_00)
         
        volume_00 = ProgrammableFilter(partFluid_00,isosurface_00)
        volume_00.PythonPath=["'C:/Users/penzo/AppData/Roaming/FreeCAD/Mod/DesignSPHysics/mod/paraview'"]
        cmd = ["from pv_volume import Volume \n",
               "#parameters \n",
               "CleanerTolerance = {} \n".format(pv_params["dp"]),
               "Volume(self,CleanerTolerance)"]
        for c in cmd:
            volume_00.Script += c
                         
        volume_00.OutputDataSetType = "vtkUnstructuredGrid"
        RenameSource('VolumeFilter',volume_00)
        # animationScene1 = GetAnimationScene()

        # timeKeeper1 = GetTimeKeeper()

        # animationScene1.PlayMode = 'Snap To TimeSteps'
        
        # if (pv_params["time_step"] != 1):
        #     animationScene1.PlayMode = 'Sequence'
        #     animationScene1.EndTime = int(animationScene1.EndTime / int(pv_params["time_step"]))* int(pv_params["time_step"])
        #     animationScene1.NumberOfFrames = int(animationScene1.EndTime / int(pv_params["time_step"])) + 1 
        
        SaveState(case + '/' + pv_params["name"] + '_State.pvsm')
        
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

clientSocket.close()

pv_state = ParaviewState(pv_params)
# clientSocket.sendto(pv_state.clientMessage.encode(), (serverName, serverPort))

