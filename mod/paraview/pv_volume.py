import os

import subprocess

from paraview.simple import *
from paraview.vtk import vtkIOLegacy

def volumeGen(fluidName,isoName,volumePath,volumeNum,tolerance):
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
    
    for cmd in [ncmd,scmd,tcmd,vcmd]:
        process = subprocess.call(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,creationflags=0x08000000)
    
    return vout

def waitFile(fn):
    
    while True:
        try:
          open(fn, "r")
          break
        except IOError:
          pass
   
def volume(parent,tolerance):
      
    out = ""
    
    fluid = parent.GetInputDataObject(0,0)
    iso = parent.GetInputDataObject(0,1)

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
                out = volumeGen(fluidName,isoName,volumePath,volumeNum,tolerance)
    elif not os.path.isdir(volumePath + "/data"):
        try:
            os.mkdir(volumePath + "/data")
        except OSError:
            print ("Creation of the directory %s failed" % volumePath)
        else:
            print ("Successfully creted the directory %s" % volumePath)
            out = volumeGen(fluidName,isoName,volumePath,volumeNum,tolerance)
    else:
        out = volumeGen(fluidName,isoName,volumePath,volumeNum,tolerance)
    
    waitFile(out)
            
    reader = vtkIOLegacy.vtkUnstructuredGridReader()
    reader.SetFileName(out)
    reader.Update()
    return reader.GetOutput()
        
    
                     