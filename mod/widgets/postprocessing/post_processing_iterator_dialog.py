# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 12:19:09 2020

@author: penzo
"""

import os
import sys

from PySide import QtGui, QtCore

class PostProcessingIteratorDialog(QtGui.QDialog):
        
    def __init__(self, post_processing_widget, parent=None):
        super().__init__(parent=parent)
        
        #self.setSizePolicy(QtGui.QSizePolicy().Expanding,QtGui.QSizePolicy().Expanding)
        self.setWindowTitle("Post processing iterators")
        
        self.progress_bar = None
        self.case_path_lines = []
                
        self.add_case_button = QtGui.QPushButton("Add case")
        self.run_button = QtGui.QPushButton("Run")
        self.cancel_button = QtGui.QPushButton("Cancel")
        
        self.add_case_button.clicked.connect(self.on_add_case)
        self.run_button.clicked.connect(self.on_run_button)
        
        self.buttons_layout = QtGui.QHBoxLayout()
        self.buttons_layout.addWidget(self.add_case_button)
        self.buttons_layout.addWidget(self.run_button)
        self.buttons_layout.addWidget(self.cancel_button)
        
        self.partfluid_checkbox = QtGui.QCheckBox("Fluid")
        self.partfixed_checkbox = QtGui.QCheckBox("Fixed")
        self.partmoving_checkbox = QtGui.QCheckBox("Moving")
        self.boundaryvtk_checkbox = QtGui.QCheckBox("BoundaryVTK")
        self.isosurface_checkbox = QtGui.QCheckBox("Isosurface")
        self.mixingindex_checkbox = QtGui.QCheckBox("MixingIndex")
        self.mixingtorque_checkbox = QtGui.QCheckBox("MixingTorque")
        
        self.partfluid_checkbox.setChecked(True)
        self.boundaryvtk_checkbox.setChecked(True)
        self.mixingtorque_checkbox.setChecked(True)
        
        self.mixingindex_checkbox.setDisabled(True)
        
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
             
        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.main_layout.addLayout(self.tools_layout)
        self.main_layout.addWidget(self.case_progress_bar)
        self.main_layout.addWidget(self.progress_bar)
        self.main_layout.addLayout(self.buttons_layout)
        
        self.setLayout(self.main_layout)
                
        self.show()
    
    def on_run_button(self):              
            
        case_counter = 0          
        for case_line in self.case_path_lines:   
            case_exit_codes = []
            if os.path.isfile(case_line.text()+'/casedata.dsphdata'):
                case_line.removeAction(case_line.remove)                
                cwd = os.getcwd()
                os.chdir(case_line.text()+'/'+case_line.text().split('/')[-1]+'_out')
                
                if self.boundaryvtk_checkbox.isChecked():
                    process_argv = ['-loadvtk *_Actual.vtk','-filexml AUTO','-motiondata .','-savevtkdata BoundaryMoving\BoundaryMoving.vtk',
                                   '-onlytype:moving','-savevtkdata Boundary.vtk','-onlytype:fixed']
                    process = QtCore.QProcess()
                    process.start(r'C:/Users/penzo/AppData/Roaming/FreeCAD/Mod/DesignSPHysics/dualsphysics/bin/BoundaryVTK_win64.exe',process_argv)
                    process.waitForFinished()
                    case_line.process_output += bytes(process.readAllStandardOutput().data()).decode()
                    case_exit_codes.append(process.exitCode())               
                self.case_progress_bar.setValue(10)
                QtCore.QCoreApplication.processEvents()
                    
                if self.isosurface_checkbox.isChecked():
                    process_argv = ['-saveiso IsoSurface\Isosurface.vtk']
                    process = QtCore.QProcess()
                    process.start(r'C:/Users/penzo/AppData/Roaming/FreeCAD/Mod/DesignSPHysics/dualsphysics/bin/IsoSurface4_win64.exe',process_argv)
                    process.waitForFinished()
                    case_line.process_output += bytes(process.readAllStandardOutput().data()).decode()
                    case_exit_codes.append(process.exitCode())
                self.case_progress_bar.setValue(20)
                QtCore.QCoreApplication.processEvents()
                        
                if self.partfluid_checkbox.isChecked():
                    process_argv = ['-savevtk PartFluid/PartFluid.vtk', '-onlytype:-moving,-fixed', '-filexml dir/AUTO', '-vars:+idp']
                    process = QtCore.QProcess()
                    process.start(r'C:/Users/penzo/AppData/Roaming/FreeCAD/Mod/DesignSPHysics/dualsphysics/bin/PartVTK_win64.exe',process_argv)
                    process.waitForFinished()
                    case_line.process_output += bytes(process.readAllStandardOutput().data()).decode()
                    case_exit_codes.append(process.exitCode())
                self.case_progress_bar.setValue(30)
                QtCore.QCoreApplication.processEvents()
                        
                if self.partfixed_checkbox.isChecked():
                    process_argv = ['-savevtk PartFixed/PartFixed.vtk', '-onlytype:-moving,-fluid', '-filexml dir/AUTO']
                    process = QtCore.QProcess()
                    process.start(r'C:/Users/penzo/AppData/Roaming/FreeCAD/Mod/DesignSPHysics/dualsphysics/bin/PartVTK_win64.exe',process_argv)
                    process.waitForFinished()
                    case_line.process_output += bytes(process.readAllStandardOutput().data()).decode()
                    case_exit_codes.append(process.exitCode())
                self.case_progress_bar.setValue(40)
                QtCore.QCoreApplication.processEvents()
                        
                if self.partmoving_checkbox.isChecked():
                    process_argv = ['-savevtk PartMoving/PartMoving.vtk', '-onlytype:-fixed,-fluid', '-filexml dir/AUTO']
                    process = QtCore.QProcess()
                    process.start(r'C:/Users/penzo/AppData/Roaming/FreeCAD/Mod/DesignSPHysics/dualsphysics/bin/PartVTK_win64.exe',process_argv)
                    process.waitForFinished()
                    case_line.process_output += bytes(process.readAllStandardOutput().data()).decode()
                    case_exit_codes.append(process.exitCode())
                self.case_progress_bar.setValue(50)
                QtCore.QCoreApplication.processEvents()
                
                if self.mixingtorque_checkbox.isChecked():
                    process_argv = ['-onlymk: 11', '-savevtk Forces/Forces.vtk']
                    process = QtCore.QProcess()
                    process.start(r'C:/Users/penzo/AppData/Roaming/FreeCAD/Mod/DesignSPHysics/dualsphysics/bin/ComputeForces4_win64.exe',process_argv)
                    process.waitForFinished(-1)
                    case_line.process_output += bytes(process.readAllStandardOutput().data()).decode()
                    self.case_progress_bar.setValue(60)
                    QtCore.QCoreApplication.processEvents()
                    if process.exitCode():
                        case_exit_codes.append(process.exitCode())                     
                    else:
                        process_argv = [case_line.text()+'/'+case_line.text().split('/')[-1]+'_out/Forces', case_line_text.split("/")[-1], '0', '0', '0']
                        process = QtCore.QProcess()
                        process.start(r'C:/Users/penzo/AppData/Roaming/FreeCAD/Mod/DesignSPHysics/dualsphysics/bin/MixingTools/MixingTorque.exe',process_argv)
                        process.waitForFinished()
                        case_line.process_output += bytes(process.readAllStandardOutput().data()).decode()
                        case_exit_codes.append(process.exitCode())  
                        self.case_progress_bar.setValue(70)
                        QtCore.QCoreApplication.processEvents()
                        
                if 1 in case_exit_codes:
                    case_line.addAction(case_line.failed,QtGui.QLineEdit().TrailingPosition)                       
                else:
                    case_line.addAction(case_line.success,QtGui.QLineEdit().TrailingPosition)
                    
                case_counter += 1
                self.case_progress_bar.setValue(100)
                self.progress_bar.setValue(100*case_counter/len(self.case_path_lines))
                QtCore.QCoreApplication.processEvents()
                       
                os.chdir(cwd)
                      
        if len(self.case_path_lines) > 0:
            self.progress_bar.setValue(100)                 
               
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