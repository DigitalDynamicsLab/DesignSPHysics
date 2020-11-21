import os

import subprocess

from paraview.simple import *
from paraview.vtk import vtkIOLegacy

def mesh_gen(fluidName,isoName,gridName,meshPath,meshNum,tolerance):
    node = r"C:\Users\penzo\Documents\DSPHProject\ConcreteMixer\MixingGen\Node\build\Release\Node.exe"
    tol = str(tolerance)
    nin = fluidName
    nout = meshPath + "/data/Mesh_{}.a.node".format(meshNum)

    ncmd = [node,tol,nin,nout]
    
    subprocess.check_call(ncmd)
    
    stl = r"C:\Users\penzo\Documents\DSPHProject\ConcreteMixer\MixingGen\STL\build\Release\STL.exe"
    sin = isoName
    sout = meshPath + "/data/Mesh_{}.stl".format(meshNum)

    scmd = [stl,sin,sout]

    subprocess.check_call(scmd)
    
    tet = r"C:\Users\penzo\Documents\DSPHProject\ConcreteMixer\MixingGen\TetGen\tetgen.exe"
    targ = "-pikNEF"
    tin = sout
    
    tcmd = [tet,targ,tin]
    
    subprocess.check_call(tcmd)
    
    return meshPath + "/data/Mesh_{}.1.vtk".format(meshNum)
   
def mesh(parent,tolerance):
      
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
    
    meshNum = fluidName.split("/")[-1].split("_")[-1].replace(".vtk","")
    meshPath = fluidName.replace(fluidName.split("/")[-1],'')
    meshPath = meshPath.replace(meshPath.split("/")[-2],'')
    
    gridName = meshPath + "/CfgInit_Grid.vtk"
    meshPath += "/Mesh" 
    
    if not os.path.isdir(meshPath):
        try:
            os.mkdir(meshPath)
        except OSError:
            print ("Creation of the directory %s failed" % meshPath)
        else:
            try:
                os.mkdir(meshPath + "/data")
            except OSError:
                print ("Creation of the directory %s failed" % meshPath)
            else:
                print ("Successfully creted the directory %s" % meshPath + "/data")
                out = mesh_gen(fluidName,isoName,gridName,meshPath,meshNum,tolerance)
    elif not os.path.isdir(meshPath + "/data"):
        try:
            os.mkdir(meshPath + "/data")
        except OSError:
            print ("Creation of the directory %s failed" % meshPath)
        else:
            print ("Successfully creted the directory %s" % meshPath)
            out = mesh_gen(fluidName,isoName,gridName,meshPath,meshNum,tolerance)
    else:
        out = mesh_gen(fluidName,isoName,gridName,meshPath,meshNum,tolerance)
                
    reader = vtkIOLegacy.vtkUnstructuredGridReader()
    reader.SetFileName(out)
    reader.Update()
    
    return reader.GetOutput()
        
    
                     