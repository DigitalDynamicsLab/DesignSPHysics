#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Advanced Post-processing classes"""

import re
import os
import sys
import time
import datetime

import FreeCAD

from mod import file_tools
from mod.dataobjects.case import Case
from mod.executable_tools import ensure_process_is_executable_or_fail

from mod.paraview.pv_tools import PvSettingsDialog

from PySide import QtGui, QtCore

class AdvancedPostProcessingDialog(QtGui.QDialog):
    
    def __init__(self, post_processing_widget, parent=None):
        super().__init__(parent=parent)
        
        self.setWindowTitle("Advanced post processing")
        
        self.case_finished = True        
        self.progress_bar = None
        self.case_counter = 0
        self.case_exit_codes = []
        self.case_path_lines = []
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.on_time_update)
                
        self.add_case_button = QtGui.QPushButton("Add case")
        self.run_button = QtGui.QPushButton("Run")
        self.cancel_button = QtGui.QPushButton("Cancel")
        self.settings_button = QtGui.QPushButton("Settings")
        
        self.buttons_layout = QtGui.QHBoxLayout()
        self.buttons_layout.addWidget(self.add_case_button)
        self.buttons_layout.addWidget(self.run_button)
        self.buttons_layout.addWidget(self.cancel_button)
        self.buttons_layout.addWidget(self.settings_button)
        
        self.add_case_button.clicked.connect(self.on_add_case)
        self.run_button.clicked.connect(self.on_run_button)
        self.cancel_button.clicked.connect(lambda: CloseDialog(self))
        self.settings_button.clicked.connect(lambda: AdvancedPostProSettings(self))
        
        self.partfluid_checkbox = QtGui.QCheckBox("Fluid")
        self.partfixed_checkbox = QtGui.QCheckBox("Fixed")
        self.partmoving_checkbox = QtGui.QCheckBox("Moving")
        self.boundaryvtk_checkbox = QtGui.QCheckBox("BoundaryVTK")
        self.isosurface_checkbox = QtGui.QCheckBox("Isosurface")
        self.mixingindex_checkbox = QtGui.QCheckBox("MixingIndex")
        self.mixingforces_checkbox = QtGui.QCheckBox("MixingForces")

        self.partfluid_checkbox.setChecked(Case.the().postpro.partfluid_checked)
        self.boundaryvtk_checkbox.setChecked(Case.the().postpro.boundaryvtk_checked)
        self.isosurface_checkbox.setChecked(Case.the().postpro.isosurface_checked)
        self.mixingindex_checkbox.setChecked(Case.the().postpro.mixingindex_checked)        
        self.mixingforces_checkbox.setChecked(Case.the().postpro.mixingforces_checked)  
        self.partfixed_checkbox.setChecked(Case.the().postpro.partfixed_checked)
        self.partmoving_checkbox.setChecked(Case.the().postpro.partmoving_checked)
        
        if self.mixingindex_checkbox.isChecked():
            self.partfluid_checkbox.setDisabled(True)
            self.isosurface_checkbox.setDisabled(True)
            
        if self.mixingforces_checkbox.isChecked():
            self.boundaryvtk_checkbox.setDisabled(True)
        
        self.mixingindex_checkbox.clicked.connect(self.on_mixingindex_checked)
        self.mixingforces_checkbox.clicked.connect(self.on_mixingforces_checked)
        
        self.partvtk_groupbox_layout = QtGui.QVBoxLayout()
        self.partvtk_groupbox_layout.addWidget(self.partfluid_checkbox)
        self.partvtk_groupbox_layout.addWidget(self.partfixed_checkbox)
        self.partvtk_groupbox_layout.addWidget(self.partmoving_checkbox)
        
        self.partvtk_groupbox = QtGui.QGroupBox("PartVTK")
        self.partvtk_groupbox.setLayout(self.partvtk_groupbox_layout)
    
        self.tools_first_column_layout = QtGui.QVBoxLayout()
        self.tools_first_column_layout.addWidget(self.boundaryvtk_checkbox)
        self.tools_first_column_layout.addWidget(self.isosurface_checkbox)
        self.tools_first_column_layout.addWidget(self.mixingindex_checkbox)
        self.tools_first_column_layout.addWidget(self.mixingforces_checkbox)
              
        self.tools_layout = QtGui.QHBoxLayout()
        self.tools_layout.addLayout(self.tools_first_column_layout)
        self.tools_layout.addWidget(self.partvtk_groupbox)
        
        self.process_label = QtGui.QLabel("Ready")
        self.time_label = QtGui.QLabel("--:--:--")
        self.progress_label = QtGui.QLabel("-")
        
        self.time_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        
        self.main_label_layout = QtGui.QHBoxLayout()
        self.main_label_layout.addWidget(self.process_label)
        self.main_label_layout.addWidget(self.time_label)
              
        self.case_progress_bar = QtGui.QProgressBar()
        self.progress_bar = QtGui.QProgressBar()
        
        self.case_progress_bar.setValue(0)
        self.progress_bar.setValue(0)
        self.run_button.clicked.connect(lambda: self.progress_bar.setValue(0))
             
        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.main_layout.addLayout(self.tools_layout)
        self.main_layout.addWidget(self.case_progress_bar)
        self.main_layout.addWidget(self.progress_bar)
        self.main_layout.addLayout(self.main_label_layout)
        self.main_layout.addWidget(self.progress_label)
        self.main_layout.addLayout(self.buttons_layout)
        
        self.setLayout(self.main_layout)
        
        case_line = CaseLine()
        case_line.setText(Case.the().path)     
        self.case_path_lines.append(case_line) 
        self.main_layout.addWidget(case_line)
        case_line.remove.triggered.connect(self.on_remove_case)
            
        self.show()
    
    def closeEvent(self,event):    
        CloseDialog(self,event)
        
    def on_mixingindex_checked(self):
        if self.mixingindex_checkbox.isChecked():
            if not self.partfluid_checkbox.isChecked():
                self.partfluid_checkbox.setChecked(True)
                self.isosurface_checkbox.setChecked(True)
            self.partfluid_checkbox.setDisabled(True)
            self.isosurface_checkbox.setDisabled(True)
        else:
            self.partfluid_checkbox.setEnabled(True)  
            self.isosurface_checkbox.setEnabled(True) 
            
    def on_mixingforces_checked(self):
        if self.mixingforces_checkbox.isChecked():
            if not self.boundaryvtk_checkbox.isChecked():
                self.boundaryvtk_checkbox.setChecked(True)
            self.boundaryvtk_checkbox.setDisabled(True)
        else:
            self.boundaryvtk_checkbox.setEnabled(True)           
    
    def on_time_update(self):
        self.time_label.setText(str(datetime.timedelta(seconds=int(time.time()-self.start_time))))
        
    def on_data_ready(self,case_line,process):
        new_output = bytes(process.readAllStandardOutput().data()).decode()
        case_line.process_output += new_output
        if len(new_output.splitlines()) > 1:
            self.progress_label.setText(new_output.splitlines()[-2][:50])
        else:
            self.progress_label.setText(new_output.splitlines()[-1][:50])
    
    def process_init(self,path,argv,name,case_line):
            process = QtCore.QProcess()
            self.running_process = process
            process.start(path,argv)
            self.process_label.setText(name)
            process.readyRead.connect(lambda: self.on_data_ready(case_line,process))
            process.finished.connect(lambda: self.on_process_finished(case_line,process,name))
            return process

    def on_process_finished(self,case_line,process,process_name):
        case_line.process_output += bytes(process.readAllStandardOutput().data()).decode()
        self.progress_label.setText(process_name + "completed.")
        self.case_exit_codes.append(process.exitCode())
    
    def boundaryvtk(self,case_line):
        self.case_progress_bar.setValue(10)
        if self.boundaryvtk_checkbox.isChecked():
            path = os.path.abspath(FreeCAD.getUserAppDataDir() + 'Mod/DesignSPHysics/dualsphysics/bin/' + Case.the().executable_paths.boundaryvtk.split('/')[-1])
            ensure_process_is_executable_or_fail(path)
            process_argv = ['-loadvtk *_Actual.vtk','-filexml AUTO','-motiondata .',
                            "-savevtkdata {}\{}.vtk".format(Case.the().pvparam.params["boundarymoving"],Case.the().pvparam.params["boundarymoving"]),
                            '-onlytype:moving',"-savevtkdata {}.vtk".format(Case.the().pvparam.params["boundaryfixed"]),'-onlytype:fixed']
            process = self.process_init(path,process_argv,"BoundaryVTK",case_line)
            process.finished.connect(lambda: self.isosurface(case_line))   
        else:
            self.isosurface(case_line)
    
    def isosurface(self,case_line):
        self.case_progress_bar.setValue(20)
        if self.isosurface_checkbox.isChecked():
            path = os.path.abspath(FreeCAD.getUserAppDataDir() + 'Mod/DesignSPHysics/dualsphysics/bin/' + Case.the().executable_paths.isosurface.split('/')[-1])
            ensure_process_is_executable_or_fail(path)
            process_argv = ["-saveiso {}\{}.vtk".format(Case.the().pvparam.params["isosurface"],Case.the().pvparam.params["isosurface"])]
            process = self.process_init(path,process_argv,"IsoSurface",case_line)
            process.finished.connect(lambda: self.partfluid(case_line))
        else:
            self.partfluid(case_line)
            
    def partfluid(self,case_line):
        self.case_progress_bar.setValue(30)
        if self.partfluid_checkbox.isChecked():
            path = os.path.abspath(FreeCAD.getUserAppDataDir() + 'Mod/DesignSPHysics/dualsphysics/bin/' + Case.the().executable_paths.partvtk.split('/')[-1])
            ensure_process_is_executable_or_fail(path)
            process_argv = ["-savevtk {}/{}.vtk".format(Case.the().pvparam.params["partfluid"],Case.the().pvparam.params["partfluid"]), 
                            '-onlytype:-moving,-fixed', '-filexml dir/AUTO', '-vars:+idp']
            process = self.process_init(path,process_argv,"PartFluid",case_line)
            process.finished.connect(lambda: self.partfixed(case_line))
        else:
            self.partfixed(case_line)
            
    def partfixed(self,case_line):
        self.case_progress_bar.setValue(40)
        if self.partfixed_checkbox.isChecked():
            path = os.path.abspath(FreeCAD.getUserAppDataDir() + 'Mod/DesignSPHysics/dualsphysics/bin/' + Case.the().executable_paths.partvtk.split('/')[-1])
            ensure_process_is_executable_or_fail(path)
            process_argv = ["-savevtk {}/{}.vtk".format(Case.the().pvparam.params["partfixed"],Case.the().pvparam.params["partfixed"]),
                            '-onlytype:-moving,-fluid', '-filexml dir/AUTO']
            process = self.process_init(path,process_argv,"PartFixed",case_line)
            process.finished.connect(lambda: self.partmoving(case_line))
        else:
            self.partmoving(case_line)
            
    def partmoving(self,case_line):
        self.case_progress_bar.setValue(50)
        if self.partmoving_checkbox.isChecked():
            path = os.path.abspath(FreeCAD.getUserAppDataDir() + 'Mod/DesignSPHysics/dualsphysics/bin/' + Case.the().executable_paths.partvtk.split('/')[-1])
            ensure_process_is_executable_or_fail(path)
            process_argv = [["-savevtk {}/{}.vtk".format(Case.the().pvparam.params["partmoving"],Case.the().pvparam.params["partmoving"]),
                            '-onlytype:-moving,-fluid', '-filexml dir/AUTO'], '-onlytype:-fixed,-fluid', '-filexml dir/AUTO']
            process = self.process_init(path,process_argv,"PartMoving",case_line)
            process.finished.connect(lambda: self.mixingindex(case_line))
        else:
            self.mixingindex(case_line)
        
    def mixingindex(self,case_line):
        self.case_progress_bar.setValue(60)
        if self.mixingindex_checkbox.isChecked():
            path = os.path.abspath(FreeCAD.getUserAppDataDir() + 'Mod/DesignSPHysics/dualsphysics/bin/MixingTools/MixingIndex.exe')
            ensure_process_is_executable_or_fail(path)
            dirin1 = Case.the().get_out_folder_path() + "/{}".format(Case.the().pvparam.params["partfluid"])
            dirin2 = Case.the().get_out_folder_path() + "/{}".format(Case.the().pvparam.params["isosurface"])
            process_argv = [dirin1,dirin2,Case.the().postpro.mixingindex_timestep,Case.the().postpro.mixingindex_x_subdiv,
                Case.the().postpro.mixingindex_y_subdiv,Case.the().postpro.mixingindex_z_subdiv,str(Case.the().execution_parameters.timeout),
                Case.the().postpro.mixingindex_spec_dir,Case.the().postpro.mixingindex_spec_div,Case.the().postpro.mixingindex_iso_surf,
                Case.the().postpro.mixingindex_part_fluid]
            process = self.process_init(path,process_argv,"MixingIndex",case_line)
            process.finished.connect(lambda: self.computeforce(case_line))
        else:
            self.computeforce(case_line)
    
    def computeforce(self,case_line): 
        self.case_progress_bar.setValue(70)
        if self.mixingforces_checkbox.isChecked():
            path = os.path.abspath(FreeCAD.getUserAppDataDir() + 'Mod/DesignSPHysics/dualsphysics/bin/' + Case.the().executable_paths.computeforces.split('/')[-1])
            ensure_process_is_executable_or_fail(path)
            process_argv = ['-onlymk:'+Case.the().postpro.computeforce_mk, "-savevtk {}/{}.vtk".format(Case.the().pvparam.params["forces"],Case.the().pvparam.params["forces"])]
            process = self.process_init(path,process_argv,"ComputeForces",case_line)
            process.finished.connect(lambda: self.mixingforces(case_line,process))
        else:
            self.case_counter += 1
            self.on_case_finished(case_line)
            self.on_run_button()
        
    def mixingforces(self,case_line,process):
        self.case_counter += 1
        self.case_progress_bar.setValue(80)
        if not process.exitCode():
            path = os.path.abspath(FreeCAD.getUserAppDataDir() + 'Mod/DesignSPHysics/dualsphysics/bin/MixingTools/MixingForces.exe')
            ensure_process_is_executable_or_fail(path)
            process_argv = [Case.the().get_out_folder_path() + "/{}".format(Case.the().pvparam.params["forces"]), case_line.text().split("/")[-1], 
                Case.the().postpro.mixingforces_x_point, Case.the().postpro.mixingforces_y_point, Case.the().postpro.mixingforces_z_point,
                Case.the().postpro.mixingforces_tau, str(Case.the().execution_parameters.timeout), 
                Case.the().get_out_folder_path() + "/{}".format(Case.the().pvparam.params["boundarymoving"]),
                Case.the().postpro.mixingforces_mesh_ref,Case.the().postpro.mixingforces_bound_vtk,Case.the().postpro.mixingforces_torque]
            process = self.process_init(path,process_argv,"MixingForces",case_line)
            process.finished.connect(lambda: self.on_case_finished(case_line))
            process.finished.connect(self.on_run_button)
        else:
            self.on_case_finished(case_line)
            self.on_run_button()
            
    def on_run_button(self):
        
        if self.case_counter == 0:
            self.start_time = time.time()
            self.on_time_update()
            self.run_button.setDisabled(True)
            Case.the().postpro.partfluid_checked = self.partfluid_checkbox.isChecked()
            Case.the().postpro.partfixed_checked = self.partfixed_checkbox.isChecked()
            Case.the().postpro.partmoving_checked = self.partmoving_checkbox.isChecked()
            Case.the().postpro.boundaryvtk_checked = self.boundaryvtk_checkbox.isChecked()
            Case.the().postpro.isosurface_checked = self.isosurface_checkbox.isChecked()
            Case.the().postpro.mixingindex_checked = self.mixingindex_checkbox.isChecked()
            Case.the().postpro.mixingforces_checked = self.mixingforces_checkbox.isChecked()
            file_tools.save_case(Case.the().path,Case.the())
            QtGui.QApplication.processEvents()
        
        if self.case_counter < len(self.case_path_lines):
            self.case_finished = False
            case_line = self.case_path_lines[self.case_counter] 
            case_line.process_output = ''
            if os.path.isfile(case_line.text()+'/casedata.dsphdata'):
                case_line.removeAction(case_line.remove)     
                case_line.removeAction(case_line.success)
                case_line.removeAction(case_line.failed)                
                
                self.cwd = os.getcwd()
                os.chdir(case_line.text()+'/'+case_line.text().split('/')[-1]+'_out')                 
                self.timer.start(1000)
                self.boundaryvtk(case_line) 
        else:
            self.progress_label.setText('Post-processing completed.')
            self.timer.stop()
            self.run_button.setEnabled(True)
            self.case_counter = 0
    
    def on_case_finished(self,case_line):
        os.chdir(self.cwd)
        self.case_finished = True
        self.process_label.setText("Ready")
        self.progress_label.setText('Case post-processing completed.')
        self.case_progress_bar.setValue(100)
        self.progress_bar.setValue(100*self.case_counter/len(self.case_path_lines))
        if 1 in self.case_exit_codes:
            case_line.addAction(case_line.failed,QtGui.QLineEdit().TrailingPosition)                       
        else:
            case_line.addAction(case_line.success,QtGui.QLineEdit().TrailingPosition)
        
    def on_add_case(self):   
        
        file_dialog = MultiSelectDirDialog()
        selected_files = file_dialog.selected_files()
               
        if selected_files is not None:
            for file_name in selected_files:
                case_line = CaseLine()
                case_line.setText(file_name)
                
                self.case_path_lines.append(case_line) 
                self.main_layout.addWidget(case_line)
                
                case_line.remove.triggered.connect(self.on_remove_case)
    
    def on_remove_case(self):
        case_line = self.case_path_lines[-1]
        self.case_path_lines.remove(case_line)
        self.main_layout.removeWidget(case_line)
        case_line.deleteLater()

class CloseDialog(QtGui.QDialog):
    def __init__(self,parent = None, event = None):
        super().__init__(parent = parent)
        
        if parent.case_finished == False:
            self.ok_button = QtGui.QPushButton('Ok')
            self.cancel_button = QtGui.QPushButton('Cancel')
            self.ok_button.clicked.connect(lambda: self.on_close_ok_button(parent,event))
                
            self.cancel_button.clicked.connect(lambda: self.close())
            if event is not None:
                self.cancel_button.clicked.connect(lambda: event.ignore())
            
            self.buttons_layout = QtGui.QHBoxLayout()
            self.buttons_layout.addWidget(self.ok_button)
            self.buttons_layout.addWidget(self.cancel_button)
            
            self.dialog_layout = QtGui.QVBoxLayout()
            self.dialog_layout.addWidget(QtGui.QLabel('Abort post-processing?'))
            self.dialog_layout.addLayout(self.buttons_layout)           
            self.setLayout(self.dialog_layout)
            
            self.exec_()
            
    def on_close_ok_button(self,parent,event):        
        parent.running_process.kill()
        parent.timer.stop()
        parent.partfluid_checkbox.setChecked(False)
        parent.boundaryvtk_checkbox.setChecked(False)
        parent.isosurface_checkbox.setChecked(False)
        parent.mixingindex_checkbox.setChecked(False)        
        parent.mixingforces_checkbox.setChecked(False)  
        parent.partfixed_checkbox.setChecked(False)
        parent.partmoving_checkbox.setChecked(False)
        parent.case_counter = 1000    
        parent.case_finished = True
        self.close()
        if event is None:
            parent.partfluid_checkbox.setChecked(Case.the().postpro.partfluid_checked)
            parent.boundaryvtk_checkbox.setChecked(Case.the().postpro.boundaryvtk_checked)
            parent.isosurface_checkbox.setChecked(Case.the().postpro.isosurface_checked)
            parent.mixingindex_checkbox.setChecked(Case.the().postpro.mixingindex_checked)        
            parent.mixingforces_checkbox.setChecked(Case.the().postpro.mixingforces_checked)  
            parent.partfixed_checkbox.setChecked(Case.the().postpro.partfixed_checked)
            parent.partmoving_checkbox.setChecked(Case.the().postpro.partmoving_checked)
                    
class AdvancedPostProSettings(QtGui.QDialog):
    def __init__(self,parent = None):
        super().__init__(parent = parent)
        
        self.setWindowTitle("Post-processing settings")
               
        self.mixingindex_timestep = QtGui.QLineEdit(Case.the().postpro.mixingindex_timestep)
        self.mixingindex_x_subdiv = QtGui.QLineEdit(Case.the().postpro.mixingindex_x_subdiv)
        self.mixingindex_y_subdiv = QtGui.QLineEdit(Case.the().postpro.mixingindex_y_subdiv)
        self.mixingindex_z_subdiv = QtGui.QLineEdit(Case.the().postpro.mixingindex_z_subdiv)
       
        self.mixingindex_spec_dir = QtGui.QComboBox()
        self.mixingindex_spec_dir.addItem("X")
        self.mixingindex_spec_dir.addItem("Y")
        self.mixingindex_spec_dir.addItem("Z")
        self.mixingindex_spec_dir.setCurrentIndex(int(Case.the().postpro.mixingindex_spec_dir))
        
        self.mixingindex_spec_div = QtGui.QComboBox()
        self.mixingindex_spec_div.addItem("Linear")
        self.mixingindex_spec_div.addItem("Alternated")
        self.mixingindex_spec_div.setCurrentIndex(int(Case.the().postpro.mixingindex_spec_div))
        
        self.mixingindex_iso_surf = QtGui.QComboBox()
        self.mixingindex_iso_surf.addItem("Disabled")
        self.mixingindex_iso_surf.addItem("Enabled")
        self.mixingindex_iso_surf.setCurrentIndex(int(Case.the().postpro.mixingindex_iso_surf))
        
        self.mixingindex_part_fluid = QtGui.QComboBox()
        self.mixingindex_part_fluid.addItem("Disabled")
        self.mixingindex_part_fluid.addItem("Enabled")      
        self.mixingindex_part_fluid.setCurrentIndex(int(Case.the().postpro.mixingindex_part_fluid))
        
        label_layout = QtGui.QVBoxLayout()
        label_layout.addWidget(QtGui.QLabel("Calculation time step:"))
        label_layout.addWidget(QtGui.QLabel("Domain X axis subdivisions:"))
        label_layout.addWidget(QtGui.QLabel("Domain Y axis subdivisions:"))
        label_layout.addWidget(QtGui.QLabel("Domain Z axis subdivisions:"))
        label_layout.addWidget(QtGui.QLabel("Direction for species subdivision:"))
        label_layout.addWidget(QtGui.QLabel("Type of species subdivision:"))
        label_layout.addWidget(QtGui.QLabel(("Update {}:").format(Case.the().pvparam.params["isosurface"])))
        label_layout.addWidget(QtGui.QLabel(("Update {}:").format(Case.the().pvparam.params["partfluid"])))
        lineedit_layout = QtGui.QVBoxLayout()
        lineedit_layout.addWidget(self.mixingindex_timestep)
        lineedit_layout.addWidget(self.mixingindex_x_subdiv)
        lineedit_layout.addWidget(self.mixingindex_y_subdiv)
        lineedit_layout.addWidget(self.mixingindex_z_subdiv)
        lineedit_layout.addWidget(self.mixingindex_spec_dir)
        lineedit_layout.addWidget(self.mixingindex_spec_div)
        lineedit_layout.addWidget(self.mixingindex_iso_surf)
        lineedit_layout.addWidget(self.mixingindex_part_fluid)
        layout = QtGui.QHBoxLayout()
        layout.addLayout(label_layout)
        layout.addLayout(lineedit_layout)
        self.mixingindex_groupbox = QtGui.QGroupBox("MixingIndex") 
        self.mixingindex_groupbox.setLayout(layout)
               
        self.computeforce_mk = QtGui.QLineEdit(Case.the().postpro.computeforce_mk)         
        self.mixingforces_x_point = QtGui.QLineEdit(Case.the().postpro.mixingforces_x_point)
        self.mixingforces_y_point = QtGui.QLineEdit(Case.the().postpro.mixingforces_y_point)
        self.mixingforces_z_point = QtGui.QLineEdit(Case.the().postpro.mixingforces_z_point)
        self.mixingforces_tau = QtGui.QLineEdit(Case.the().postpro.mixingforces_tau)
        self.mixingforces_mesh_ref = QtGui.QLineEdit(Case.the().postpro.mixingforces_mesh_ref)
        
        self.mixingforces_bound_vtk = QtGui.QComboBox()
        self.mixingforces_bound_vtk.addItem("Disabled")
        self.mixingforces_bound_vtk.addItem("Moving")
        self.mixingforces_bound_vtk.setCurrentIndex(int(Case.the().postpro.mixingforces_bound_vtk))
        
        self.mixingforces_torque = QtGui.QComboBox()
        self.mixingforces_torque.addItem("Disabled")
        self.mixingforces_torque.addItem("Enabled")     
        self.mixingforces_torque.setCurrentIndex(int(Case.the().postpro.mixingforces_torque))
        
        self.mixingforces_tau.setToolTip("motor_torque = mixer_torque/tau")
        self.mixingforces_mesh_ref.setToolTip("New mesh will have 4xFactor new triangles")
        
        label_layout = QtGui.QVBoxLayout()
        label_layout.addWidget(QtGui.QLabel("Rotor Mk:"))
        label_layout.addWidget(QtGui.QLabel("Axis X point coordinate:"))
        label_layout.addWidget(QtGui.QLabel("Axis Y point coordinate:"))
        label_layout.addWidget(QtGui.QLabel("Axis Z point coordinate:"))
        label_layout.addWidget(QtGui.QLabel("Reduction ratio:"))
        label_layout.addWidget(QtGui.QLabel("Mesh refinement factor:"))
        label_layout.addWidget(QtGui.QLabel("Update BoundaryVTK:"))
        label_layout.addWidget(QtGui.QLabel("Torque computation:"))        
        lineedit_layout = QtGui.QVBoxLayout()
        lineedit_layout.addWidget(self.computeforce_mk)
        lineedit_layout.addWidget(self.mixingforces_x_point)
        lineedit_layout.addWidget(self.mixingforces_y_point)
        lineedit_layout.addWidget(self.mixingforces_z_point)
        lineedit_layout.addWidget(self.mixingforces_tau)
        lineedit_layout.addWidget(self.mixingforces_mesh_ref)
        lineedit_layout.addWidget(self.mixingforces_bound_vtk)
        lineedit_layout.addWidget(self.mixingforces_torque)     
        layout = QtGui.QHBoxLayout()
        layout.addLayout(label_layout)
        layout.addLayout(lineedit_layout)
        self.mixingforces_groupbox = QtGui.QGroupBox("MixingForces") 
        self.mixingforces_groupbox.setLayout(layout)        
        
        
        self.apply_button = QtGui.QPushButton("Apply")
        self.other_button = QtGui.QPushButton("Others")
        self.apply_button.clicked.connect(self.on_apply_button)
        self.other_button.clicked.connect(lambda: PvSettingsDialog(self))
        
        self.buttons_layout = QtGui.QHBoxLayout()
        self.buttons_layout.addWidget(self.apply_button)
        self.buttons_layout.addWidget(self.other_button)
        
        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.addWidget(self.mixingindex_groupbox)
        self.main_layout.addWidget(self.mixingforces_groupbox)
        self.main_layout.addLayout(self.buttons_layout)
        self.main_layout.addWidget(QtGui.QLabel("Settings will be saved only for loaded case but used\nin all case added to Advanced post-processing."))
        
        self.setLayout(self.main_layout)
        
        self.show()
        
    def on_apply_button(self):
        Case.the().postpro.mixingindex_timestep = self.mixingindex_timestep.text()
        Case.the().postpro.mixingindex_x_subdiv = self.mixingindex_x_subdiv.text()
        Case.the().postpro.mixingindex_y_subdiv = self.mixingindex_y_subdiv.text()
        Case.the().postpro.mixingindex_z_subdiv = self.mixingindex_z_subdiv.text() 
        Case.the().postpro.mixingindex_spec_dir = str(self.mixingindex_spec_dir.currentIndex())
        Case.the().postpro.mixingindex_spec_div = str(self.mixingindex_spec_div.currentIndex())
        Case.the().postpro.mixingindex_iso_surf = str(self.mixingindex_iso_surf.currentIndex())
        Case.the().postpro.mixingindex_part_fluid = str(self.mixingindex_part_fluid.currentIndex())
        
        Case.the().postpro.computeforce_mk = self.computeforce_mk.text()
        
        Case.the().postpro.mixingforces_x_point = self.mixingforces_x_point.text()
        Case.the().postpro.mixingforces_y_point = self.mixingforces_y_point.text()
        Case.the().postpro.mixingforces_z_point = self.mixingforces_z_point.text()
        Case.the().postpro.mixingforces_tau = str(eval(self.mixingforces_tau.text()))
        Case.the().postpro.mixingforces_mesh_ref = self.mixingforces_mesh_ref.text()
        Case.the().postpro.mixingforces_bound_vtk = str(self.mixingforces_bound_vtk.currentIndex())
        Case.the().postpro.mixingforces_torque = str(self.mixingforces_torque.currentIndex())
        
        file_tools.save_case(Case.the().path,Case.the())
        
        self.close()
                         
class CaseLine(QtGui.QLineEdit):
    
    def __init__(self,parent = None):
        super().__init__(parent = parent)
        
        self.process_output = ''
        self.success = QtGui.QAction(self)
        self.success.setIcon(QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_DialogApplyButton))
        self.success.triggered.connect(self.on_output_message)
        self.failed = QtGui.QAction(self)
        self.failed.setIcon(QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_DialogCancelButton))
        self.failed.triggered.connect(self.on_output_message)
        self.remove = QtGui.QAction(self)
        self.remove.setIcon(QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_LineEditClearButton))
        
        #self.case_path_lines[0].addAction(self.remove_icon,QtGui.QLineEdit().TrailingPosition)
        #self.case_path_lines[0].removeAction(self.success_icon)
        
        self.addAction(self.remove,QtGui.QLineEdit().TrailingPosition)
    
    def on_output_message(self):
        output_message = QtGui.QDialog(self)
        output_message.setWindowTitle(self.text().split('/')[-1].replace('_out',''))
        output_message.setMinimumHeight(600)
        output_message.setMinimumWidth(600)
        output_message_layout = QtGui.QVBoxLayout()
        output_message_text_box = QtGui.QTextEdit()
        output_message_text_box.setReadOnly(True)
        output_message_layout.addWidget(output_message_text_box)
        output_message_text_box.setText(self.process_output)
        output_message.setLayout(output_message_layout)
        output_message.show()
        
class MultiSelectDirDialog(QtGui.QFileDialog):

    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self.setFileMode(QtGui.QFileDialog.DirectoryOnly)
        self.setOption(QtGui.QFileDialog.DontUseNativeDialog, True)
        file_view = self.findChild(QtGui.QListView, 'listView')
        
        # to make it possible to select multiple directories:
        if file_view:
            file_view.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        f_tree_view = self.findChild(QtGui.QTreeView)
        if f_tree_view:
            f_tree_view.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
    
    def selected_files(self):
        if self.exec():
            paths = self.selectedFiles()     
            return paths
        else:
            return None