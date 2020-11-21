import os

import subprocess

from paraview.simple import *
from paraview.vtk import vtkIOLegacy

def exec_volume_gen(fluidName,isoName,gridName,volumePath,volumeNum,tolerance):
    node = r"C:\Users\penzo\Documents\DSPHProject\ConcreteMixer\MixingGen\Node\build\Release\Node.exe"
    tol = str(tolerance)
    nin = fluidName
    nout1 = volumePath + "/data/Volume_{}.a.node".format(volumeNum)
    nout2 = volumePath + "/data/Volume_{}.vtk".format(volumeNum)

    ncmd = [node,tol,nin,nout1,nout2]

    stl = r"C:\Users\penzo\Documents\DSPHProject\ConcreteMixer\MixingGen\STL\build\Release\STL.exe"
    sin = isoName
    sout = volumePath + "/data/Volume_{}.stl".format(volumeNum)

    scmd = [stl,sin,sout]

    tet = r"C:\Users\penzo\Documents\DSPHProject\ConcreteMixer\MixingGen\TetGen\tetgen.exe"
    targ = "-pikNEF"
    tin = sout
    
    tcmd = [tet,targ,tin]

    vol = r"C:\Users\penzo\Documents\DSPHProject\ConcreteMixer\MixingGen\Volume\build\Release\Volume.exe"
    vin1 = sin
    vin2 = nout2
    vin3 = volumePath + "/data/Volume_{}.1.vtk".format(volumeNum)
    vout = volumePath + "/MVolume_{}.vtk".format(volumeNum)
    
    vcmd = [vol,vin1,vin2,vin3,vout]
    
    loc = r"C:\Users\penzo\Documents\DSPHProject\ConcreteMixer\MixingGen\LocMix\build\Release\LocMix.exe"
    lin1 = nin
    lin2 = gridName
    lout = vout

    lcmd = [loc,lin1,lin2,lout]

    for cmd in [ncmd,scmd,tcmd,vcmd,lcmd]:
        process = subprocess.call(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,creationflags=0x08000000)
    
    return lout

def waitFile(fn):
    
    while True:
        try:
          open(fn, "r")
          break
        except IOError:
          pass
   
def volume_gen(parent,tolerance):
      
    out = ""
    
    if parent.GetInputDataObject(0,0).GetNumberOfPoints() == parent.GetInputDataObject(0,0).GetNumberOfCells():
        fluid = parent.GetInputDataObject(0,0)
        iso = parent.GetInputDataObject(0,1)
    else:
        fluid = parent.GetInputDataObject(0,1)
        iso = parent.GetInputDataObject(0,0)

    fluidName=''
    fluidInfo = fluid.GetFieldData().GetArray("FileInfo")
    for n in range(0,fluidInfo.GetNumberOfValues()):
        fluidName+=str(fluidInfo.GetVariantValue(n))
    
    isoName=''
    isoInfo = iso.GetFieldData().GetArray("FileInfo")
    for n in range(0,isoInfo.GetNumberOfValues()):
        isoName+=str(isoInfo.GetVariantValue(n))
    
    volumeNum = fluidName.split("/")[-1].split("_")[-1].replace(".vtk","")
    volumePath = fluidName.replace(fluidName.split("/")[-1],'')
    volumePath = volumePath.replace(volumePath.split("/")[-2],'')
    
    gridName = volumePath + "/CfgInit_Grid.vtk"
    volumePath += "/Volume" 
    
    if not os.path.isdir(volumePath):
        try:
            os.mkdir(volumePath)
        except OSError:
            print ("Creation of the directory %s failed" % volumePath)
        else:
            try:
                os.mkdir(volumePath + "/data")
            except OSError:
                print ("Creation of the directory %s failed" % volumePath)
            else:
                print ("Successfully creted the directory %s" % volumePath + "/data")
                out = exec_volume_gen(fluidName,isoName,gridName,volumePath,volumeNum,tolerance)
    elif not os.path.isdir(volumePath + "/data"):
        try:
            os.mkdir(volumePath + "/data")
        except OSError:
            print ("Creation of the directory %s failed" % volumePath)
        else:
            print ("Successfully creted the directory %s" % volumePath)
            out = exec_volume_gen(fluidName,isoName,gridName,volumePath,volumeNum,tolerance)
    else:
        out = exec_volume_gen(fluidName,isoName,gridName,volumePath,volumeNum,tolerance)
    
    waitFile(out)
            
    reader = vtkIOLegacy.vtkUnstructuredGridReader()
    reader.SetFileName(out)
    reader.Update()
    
    return reader.GetOutput()
        
    
                     