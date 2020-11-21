from paraview.simple import*

sources = []
for i in GetSources():
     sources.append(GetSources()[i])
volume_00 = ProgrammableFilter(sources[1],sources[0])
volume_00.PythonPath=["'C:/Users/penzo/AppData/Roaming/FreeCAD/Mod/DesignSPHysics/mod/paraview/macros'"]
volume_00.OutputDataSetType = "vtkUnstructuredGrid"    
volume_00.Script = "from pv_volume import volume_gen\nvolume = volume_gen(self,CleanerTolerance[0])\nself.GetOutput(0).DeepCopy(volume)\n"   
volume_00.RequestInformationScript = "self.ClearParameters()\nself.AddParameter('CleanerTolerance', '0')\n"                                    
RenameSource('Volume',volume_00)