#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Fluid Mixing Post Processing Dialog """

from os import getcwd, chdir
from os.path import dirname, abspath
from PySide.QtGui import QDialog, QTextEdit, QLabel, QGroupBox
from PySide.QtGui import QGridLayout, QDesktopWidget, QPushButton, QSpinBox
from PySide.QtCore import Qt, QProcess

from mod.dataobjects.case import Case

class MixingToolDialog(QDialog):
    
    def __init__(self, post_processing_widget, parent=None):
        super().__init__(parent = parent)
        
        self.setModal(False)
        self.title = 'MixingTool post processing'
        self.left = 0
        self.top = 0
        self.width = 600
        self.height = 400
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
              
        self.process_output_textbox = QTextEdit()         
        
        self.launch_mixing_tool_pushbutton = QPushButton('Calculate')
        self.cancel_process_pushbutton = QPushButton('Cancel') 
        self.launch_boundaryVTK_pushbutton = QPushButton('Launch BoundaryVTK')  
        
        variance_calculation_step_label = QLabel('Variance calculation step:')     
        self.variance_calculation_step_spinbox = QSpinBox()
        
        self.process_output_textbox.setReadOnly(True)
      
        self.variance_calculation_step_spinbox.setFixedWidth(75)
        variance_calculation_step_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.variance_calculation_step_spinbox.setValue(10)    
        
        self.launch_mixing_tool_pushbutton.clicked.connect(self.launch_mixing_tool)
        #self.abort_calculator.clicked.connect(self.stop_calculator)
        self.launch_boundaryVTK_pushbutton.clicked.connect(self.launch_boundaryVTK_tool)
        
        self.init_domain_subdivisions_parameters_groupbox()
            
        self.layout = QGridLayout()
        self.layout.addWidget(self.process_output_textbox,0,0,1,4)
        self.layout.addWidget(self.launch_mixing_tool_pushbutton,2,0,1,1)
        self.layout.addWidget(self.cancel_process_pushbutton,2,3,1,1)
        self.layout.addWidget(self.domain_subdivisions_parameters_groupbox,3,0,1,4)
        self.layout.addWidget(self.launch_boundaryVTK_pushbutton,4,3,1,1)
        self.layout.addWidget(self.variance_calculation_step_spinbox,4,2,1,1)
        self.layout.addWidget(variance_calculation_step_label,4,0,1,2)
        self.setLayout(self.layout)
        
        self.center()  
        
        #self.show()
        self.exec_()
        
    #def closeEvent(self,event):
        #QApplication.quit()
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def init_domain_subdivisions_parameters_groupbox(self):
        self.domain_subdivisions_parameters_groupbox = QGroupBox()
        self.domain_subdivisions_parameters_groupbox_layout = QGridLayout()
        self.domain_subdivisions_parameters_groupbox.setTitle('Domain subdivisions')
        self.subdivisions_x_axis = QSpinBox()
        self.subdivisions_y_axis = QSpinBox()
        self.subdivisions_z_axis = QSpinBox()
        self.subdivisions_x_axis.setValue(30)
        self.subdivisions_y_axis.setDisabled(True)
        self.subdivisions_z_axis.setDisabled(True)
        x_axis_label = QLabel('X-axis:')
        y_axis_label = QLabel('Y-axis:')
        z_axis_label = QLabel('Z-axis:')
        x_axis_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        y_axis_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        z_axis_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.domain_subdivisions_parameters_groupbox_layout.addWidget(x_axis_label,0,0,1,1)
        self.domain_subdivisions_parameters_groupbox_layout.addWidget(y_axis_label,0,2,1,1)
        self.domain_subdivisions_parameters_groupbox_layout.addWidget(z_axis_label,0,4,1,1)
        self.domain_subdivisions_parameters_groupbox_layout.addWidget(self.subdivisions_x_axis,0,1,1,1)
        self.domain_subdivisions_parameters_groupbox_layout.addWidget(self.subdivisions_y_axis,0,3,1,1)
        self.domain_subdivisions_parameters_groupbox_layout.addWidget(self.subdivisions_z_axis,0,5,1,1)
        self.domain_subdivisions_parameters_groupbox.setLayout(self.domain_subdivisions_parameters_groupbox_layout)
     
    
    def on_data_ready(self,process):
        self.process_output_textbox.append(bytes(process.readAll().data()).decode())
        
    def launch_mixing_tool(self):
        
        case_name = Case.the().path.split('/')[-1]
        case_part_fluid_directory = Case.the().path+'/'+case_name+'_out/PartFluid'
        
        MixingTool_process_full_path = dirname(abspath(__file__)).replace('mod\widgets\postprocessing','/dualsphysics/bin/MixingTool/MixingTool.exe')
        MixingTool_process_argv = [case_part_fluid_directory,
                                   str(self.variance_calculation_step_spinbox.value()),
                                   str(self.subdivisions_x_axis.value())]
        MixingTool_process = QProcess()
        MixingTool_process.start(MixingTool_process_full_path,MixingTool_process_argv)         
        MixingTool_process.readyRead.connect(lambda: self.on_data_ready(MixingTool_process))
            
    def launch_boundaryVTK_tool(self):
           
        cwd = getcwd()
        case_name = Case.the().path.split('/')[-1]
        chdir(Case.the().path+'/'+case_name+'_out')
        
        BoundaryVTK_process_full_path = dirname(abspath(__file__)).replace('mod\widgets\postprocessing',Case.the().executable_paths.boundaryvtk)
        BoundaryVTK_process_argv = ['-loadvtk *_Actual.vtk','-filexml AUTO','-motiondata .','-savevtkdata BoundaryMoving\BoundaryMoving.vtk',
                                   '-onlytype:moving','-savevtkdata Boundary.vtk','-onlytype:fixed']
        BoundaryVTK_process = QProcess()
        BoundaryVTK_process.start(BoundaryVTK_process_full_path,BoundaryVTK_process_argv)
        BoundaryVTK_process.readyRead.connect(lambda: self.on_data_ready(BoundaryVTK_process))
        
        chdir(cwd)