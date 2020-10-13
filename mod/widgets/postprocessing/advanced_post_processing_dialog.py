# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 12:19:09 2020

@author: penzo
"""

import os
import sys

import FreeCAD

from mod import file_tools
from mod.dataobjects.case import Case
from mod.executable_tools import ensure_process_is_executable_or_fail

from PySide import QtGui, QtCore

class AdvancedPostProcessingDialog(QtGui.QDialog):
        
    def __init__(self, post_processing_widget, parent=None):
        super().__init__(parent=parent)
        
        self.setWindowTitle("Post processing iterators")
                    
        self.progress_bar = None
        self.case_counter = 0
        self.case_exit_codes = []
        self.case_path_lines = []
                
        self.add_case_button = QtGui.QPushButton("Add case")
        self.run_button = QtGui.QPushButton("Run")
        self.settings_button = QtGui.QPushButton("Settings")
        
        self.buttons_layout = QtGui.QHBoxLayout()
        self.buttons_layout.addWidget(self.add_case_button)
        self.buttons_layout.addWidget(self.run_button)
        self.buttons_layout.addWidget(self.settings_button)
        
        self.add_case_button.clicked.connect(self.on_add_case)
        self.run_button.clicked.connect(self.on_run_button)
        self.settings_button.clicked.connect(lambda: AdvancedPostProSettings(self))
        
        self.partfluid_checkbox = QtGui.QCheckBox("Fluid")
        self.partfixed_checkbox = QtGui.QCheckBox("Fixed")
        self.partmoving_checkbox = QtGui.QCheckBox("Moving")
        self.boundaryvtk_checkbox = QtGui.QCheckBox("BoundaryVTK")
        self.isosurface_checkbox = QtGui.QCheckBox("Isosurface")
        self.mixingindex_checkbox = QtGui.QCheckBox("MixingIndex")
        self.mixingtorque_checkbox = QtGui.QCheckBox("MixingTorque")

        self.partfluid_checkbox.setChecked(True)
        self.boundaryvtk_checkbox.setChecked(True)
        self.isosurface_checkbox.setChecked(True)
        self.mixingindex_checkbox.setChecked(True)        
        self.mixingtorque_checkbox.setChecked(True)    
    
        self.partfluid_checkbox.setDisabled(True)
        
        self.mixingindex_checkbox.clicked.connect(self.on_mixingindex_checked)
        
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
        self.tools_first_column_layout.addWidget(self.mixingtorque_checkbox)
              
        self.tools_layout = QtGui.QHBoxLayout()
        self.tools_layout.addLayout(self.tools_first_column_layout)
        self.tools_layout.addWidget(self.partvtk_groupbox)
        
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
        self.main_layout.addLayout(self.buttons_layout)
        
        self.setLayout(self.main_layout)
        
        case_line = CaseLine()
        case_line.setText(Case.the().path)     
        self.case_path_lines.append(case_line) 
        self.main_layout.addWidget(case_line)
        case_line.remove.triggered.connect(self.on_remove_case)
                
        self.show()
    
    def on_mixingindex_checked(self):
        if self.mixingindex_checkbox.isChecked():
            if not self.partfluid_checkbox.isChecked():
                self.partfluid_checkbox.setChecked(True)
            self.partfluid_checkbox.setDisabled(True)
        else:
            self.partfluid_checkbox.setEnabled(True)            
  
    def on_process_finished(self,case_line,process):
        case_line.process_output += bytes(process.readAllStandardOutput().data()).decode()
        self.case_exit_codes.append(process.exitCode())
    
    def boundaryvtk(self,case_line):
        self.case_progress_bar.setValue(10)
        if self.boundaryvtk_checkbox.isChecked():
            path = os.path.abspath(FreeCAD.getUserAppDataDir() + 'Mod/DesignSPHysics/dualsphysics/bin/' + Case.the().executable_paths.boundaryvtk.split('/')[-1])
            ensure_process_is_executable_or_fail(path)
            process_argv = ['-loadvtk *_Actual.vtk','-filexml AUTO','-motiondata .','-savevtkdata BoundaryMoving\BoundaryMoving.vtk',
                           '-onlytype:moving','-savevtkdata Boundary.vtk','-onlytype:fixed']
            process = QtCore.QProcess()
            process.start(path,process_argv)
            process.finished.connect(lambda: self.on_process_finished(case_line,process))
            process.finished.connect(lambda: self.isosurface(case_line))   
        else:
            self.isosurface(case_line)
    
    def isosurface(self,case_line):
        self.case_progress_bar.setValue(20)
        if self.isosurface_checkbox.isChecked():
            path = os.path.abspath(FreeCAD.getUserAppDataDir() + 'Mod/DesignSPHysics/dualsphysics/bin/' + Case.the().executable_paths.isosurface.split('/')[-1])
            ensure_process_is_executable_or_fail(path)
            process_argv = ['-saveiso IsoSurface\Isosurface.vtk']
            process = QtCore.QProcess()
            process.start(path,process_argv)
            process.finished.connect(lambda: self.on_process_finished(case_line,process))
            process.finished.connect(lambda: self.partfluid(case_line))
        else:
            self.partfluid(case_line)
            
    def partfluid(self,case_line):
        self.case_progress_bar.setValue(30)
        if self.partfluid_checkbox.isChecked():
            path = os.path.abspath(FreeCAD.getUserAppDataDir() + 'Mod/DesignSPHysics/dualsphysics/bin/' + Case.the().executable_paths.partvtk.split('/')[-1])
            ensure_process_is_executable_or_fail(path)
            process_argv = ['-savevtk PartFluid/PartFluid.vtk', '-onlytype:-moving,-fixed', '-filexml dir/AUTO', '-vars:+idp']
            process = QtCore.QProcess()
            process.start(path,process_argv)
            process.finished.connect(lambda: self.on_process_finished(case_line,process))
            process.finished.connect(lambda: self.partfixed(case_line))
        else:
            self.partfixed(case_line)
            
    def partfixed(self,case_line):
        self.case_progress_bar.setValue(40)
        if self.partfixed_checkbox.isChecked():
            path = os.path.abspath(FreeCAD.getUserAppDataDir() + 'Mod/DesignSPHysics/dualsphysics/bin/' + Case.the().executable_paths.partvtk.split('/')[-1])
            ensure_process_is_executable_or_fail(path)
            process_argv = ['-savevtk PartFixed/PartFixed.vtk', '-onlytype:-moving,-fluid', '-filexml dir/AUTO']
            process = QtCore.QProcess()
            process.start(path,process_argv)
            process.finished.connect(lambda: self.on_process_finished(case_line,process))
            process.finished.connect(lambda: self.partmoving(case_line))
        else:
            self.partmoving(case_line)
            
    def partmoving(self,case_line):
        self.case_progress_bar.setValue(50)
        if self.partmoving_checkbox.isChecked():
            path = os.path.abspath(FreeCAD.getUserAppDataDir() + 'Mod/DesignSPHysics/dualsphysics/bin/' + Case.the().executable_paths.partvtk.split('/')[-1])
            ensure_process_is_executable_or_fail(path)
            process_argv = ['-savevtk PartMoving/PartMoving.vtk', '-onlytype:-fixed,-fluid', '-filexml dir/AUTO']
            process = QtCore.QProcess()
            process.start(path,process_argv)
            process.finished.connect(lambda: self.on_process_finished(case_line,process))
            process.finished.connect(lambda: self.mixingindex(case_line))
        else:
            self.mixingindex(case_line)
        
    def mixingindex(self,case_line):
        self.case_progress_bar.setValue(60)
        if self.mixingindex_checkbox.isChecked():
            path = os.path.abspath(FreeCAD.getUserAppDataDir() + 'Mod/DesignSPHysics/dualsphysics/bin/MixingTools/MixingIndex.exe')
            ensure_process_is_executable_or_fail(path)
            dirin1 = Case.the().path + '/' + Case.the().path.split('/')[-1] + '_out/PartFluid'
            dirin2 = Case.the().path + '/' + Case.the().path.split('/')[-1] + '_out/IsoSurface'
            process_argv = [dirin1,dirin2,Case.the().postpro.mixingindex_timestep,Case.the().postpro.mixingindex_x_subdiv,
                Case.the().postpro.mixingindex_y_subdiv,Case.the().postpro.mixingindex_z_subdiv]
            process = QtCore.QProcess()
            process.start(path,process_argv)
            process.finished.connect(lambda: self.on_process_finished(case_line,process))
            process.finished.connect(lambda: self.computeforce(case_line))
        else:
            self.computeforce(case_line)
    
    def computeforce(self,case_line): 
        self.case_progress_bar.setValue(70)
        if self.mixingtorque_checkbox.isChecked():
            path = os.path.abspath(FreeCAD.getUserAppDataDir() + 'Mod/DesignSPHysics/dualsphysics/bin/' + Case.the().executable_paths.computeforces.split('/')[-1])
            ensure_process_is_executable_or_fail(path)
            process_argv = ['-onlymk:'+Case.the().postpro.computeforce_mk, '-savevtk Forces/Forces.vtk']
            process = QtCore.QProcess()
            process.start(path,process_argv)
            process.finished.connect(lambda: self.on_process_finished(case_line,process))
            process.finished.connect(lambda: self.mixingtorque(case_line,process))
        else:
            self.mixingtorque(case_line)
        
    def mixingtorque(self,case_line,process):
        self.case_counter += 1
        self.case_progress_bar.setValue(80)
        if not process.exitCode():
            path = os.path.abspath(FreeCAD.getUserAppDataDir() + 'Mod/DesignSPHysics/dualsphysics/bin/MixingTools/MixingTorque.exe')
            ensure_process_is_executable_or_fail(path)
            process_argv = [case_line.text()+'/'+case_line.text().split('/')[-1]+'_out/Forces', case_line.text().split("/")[-1], 
                Case.the().postpro.mixingtorque_x_point, Case.the().postpro.mixingtorque_y_point, Case.the().postpro.mixingtorque_z_point]
            process = QtCore.QProcess()
            process.start(path,process_argv)
            process.finished.connect(lambda: self.on_process_finished(case_line,process))
            process.finished.connect(lambda: self.on_case_finished(case_line))
            process.finished.connect(self.on_run_button)
        else:
            self.on_case_finished(case_line)
            self.on_run_button()
            
    def on_run_button(self): 
        
        if self.case_counter < len(self.case_path_lines):
            case_line = self.case_path_lines[self.case_counter] 
            if os.path.isfile(case_line.text()+'/casedata.dsphdata'):
                case_line.removeAction(case_line.remove)                
                self.cwd = os.getcwd()
                os.chdir(case_line.text()+'/'+case_line.text().split('/')[-1]+'_out')         
                self.boundaryvtk(case_line) 
        else:
            self.case_counter = 0
    
    def on_case_finished(self,case_line):
        os.chdir(self.cwd)
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
                #case_line.setCursorPosition(0)
                
                self.case_path_lines.append(case_line) 
                self.main_layout.addWidget(case_line)
                
                #case_line.remove.triggered.connect()
                case_line.remove.triggered.connect(self.on_remove_case)
    
    def on_remove_case(self):
        case_line = self.case_path_lines[-1]
        self.case_path_lines.remove(case_line)
        self.main_layout.removeWidget(case_line)
        case_line.deleteLater()

class AdvancedPostProSettings(QtGui.QDialog):
    def __init__(self,parent = None):
        super().__init__(parent = parent)
               
        self.mixingindex_timestep = QtGui.QLineEdit(Case.the().postpro.mixingindex_timestep)
        self.mixingindex_x_subdiv = QtGui.QLineEdit(Case.the().postpro.mixingindex_x_subdiv)
        self.mixingindex_y_subdiv = QtGui.QLineEdit(Case.the().postpro.mixingindex_y_subdiv)
        self.mixingindex_z_subdiv = QtGui.QLineEdit(Case.the().postpro.mixingindex_z_subdiv)
        
        label_layout = QtGui.QVBoxLayout()
        label_layout.addWidget(QtGui.QLabel("Calculation time step:"))
        label_layout.addWidget(QtGui.QLabel("Domain X axis subdivisions:"))
        label_layout.addWidget(QtGui.QLabel("Domain Y axis subdivisions:"))
        label_layout.addWidget(QtGui.QLabel("Domain Z axis subdivisions:"))
        lineedit_layout = QtGui.QVBoxLayout()
        lineedit_layout.addWidget(self.mixingindex_timestep)
        lineedit_layout.addWidget(self.mixingindex_x_subdiv)
        lineedit_layout.addWidget(self.mixingindex_y_subdiv)
        lineedit_layout.addWidget(self.mixingindex_z_subdiv)
        layout = QtGui.QHBoxLayout()
        layout.addLayout(label_layout)
        layout.addLayout(lineedit_layout)
        self.mixingindex_groupbox = QtGui.QGroupBox("MixingIndex") 
        self.mixingindex_groupbox.setLayout(layout)
               
        self.computeforce_mk = QtGui.QLineEdit(Case.the().postpro.computeforce_mk)         
        self.mixingtorque_x_point = QtGui.QLineEdit(Case.the().postpro.mixingtorque_x_point)
        self.mixingtorque_y_point = QtGui.QLineEdit(Case.the().postpro.mixingtorque_y_point)
        self.mixingtorque_z_point = QtGui.QLineEdit(Case.the().postpro.mixingtorque_z_point)
    
        label_layout = QtGui.QVBoxLayout()
        label_layout.addWidget(QtGui.QLabel("Rotor Mk:"))
        label_layout.addWidget(QtGui.QLabel("Axis X point coordinate:"))
        label_layout.addWidget(QtGui.QLabel("Axis Y point coordinate:"))
        label_layout.addWidget(QtGui.QLabel("Axis Z point coordinate:"))
        lineedit_layout = QtGui.QVBoxLayout()
        lineedit_layout.addWidget(self.computeforce_mk)
        lineedit_layout.addWidget(self.mixingtorque_x_point)
        lineedit_layout.addWidget(self.mixingtorque_y_point)
        lineedit_layout.addWidget(self.mixingtorque_z_point)
        layout = QtGui.QHBoxLayout()
        layout.addLayout(label_layout)
        layout.addLayout(lineedit_layout)
        self.mixingtorque_groupbox = QtGui.QGroupBox("MixingTorque") 
        self.mixingtorque_groupbox.setLayout(layout)        
        
        self.apply_button = QtGui.QPushButton("Apply")
        self.apply_button.clicked.connect(self.on_apply_button)
        
        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.addWidget(self.mixingindex_groupbox)
        self.main_layout.addWidget(self.mixingtorque_groupbox)
        self.main_layout.addWidget(self.apply_button)
        
        self.setLayout(self.main_layout)
        
        self.show()
        
    def on_apply_button(self):
        Case.the().postpro.mixingindex_timestep = self.mixingindex_timestep.text()
        Case.the().postpro.mixingindex_x_subdiv = self.mixingindex_x_subdiv.text()
        Case.the().postpro.mixingindex_y_subdiv = self.mixingindex_y_subdiv.text()
        Case.the().postpro.mixingindex_z_subdiv = self.mixingindex_z_subdiv.text() 
        
        Case.the().postpro.computeforce_mk = self.computeforce_mk.text()
        
        Case.the().postpro.mixingtorque_x_point = self.mixingtorque_x_point.text()
        Case.the().postpro.mixingtorque_y_point = self.mixingtorque_y_point.text()
        Case.the().postpro.mixingtorque_z_point = self.mixingtorque_z_point.text()
        
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
        output_message.setMinimumHeight(600)
        output_message.setMinimumWidth(600)
        output_message_layout = QtGui.QVBoxLayout()
        output_message_text_box = QtGui.QTextEdit()
        output_message_layout.addWidget(output_message_text_box)
        output_message_text_box.append(self.process_output)
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