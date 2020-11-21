from paraview.vtk import vtkDoubleArray

def slice_data(parent):
    
    slicePoly = parent.GetInputDataObject(0,0)
    
    if not slicePoly.GetPointData().GetArray("AvgCoordNum"):
        avgCoord = vtkDoubleArray()
        avgCoord.SetNumberOfValues(slicePoly.GetNumberOfPoints())
        avgCoord.SetName("AvgCoordNum")
        avgCoord.Fill(0)
        slicePoly.GetPointData().AddArray(avgCoord)
    else:
        slicePoly.GetPointData().GetArray("AvgCoordNum").Fill(0)
        
    avgNum = 0
    for i in range(0,slicePoly.GetNumberOfPoints()):
        avgNum += slicePoly.GetPointData().GetArray("CoordNum").GetTuple1(i)
    
    if slicePoly.GetNumberOfPoints() > 0:
        avgNum = avgNum / slicePoly.GetNumberOfPoints()
    
    slicePoly.GetPointData().GetArray("AvgCoordNum").Fill(avgNum)
    
    return slicePoly