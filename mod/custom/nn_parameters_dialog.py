#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Non Newtonian Parameters Dialog """

from PySide.QtGui import QApplication, QLabel, QWidget, QPushButton
from PySide.QtGui import QDesktopWidget, QTabWidget, QLineEdit, QGridLayout
from PySide.QtGui import QComboBox, QDialog

from mod.dialog_tools import warning_dialog

from mod.custom.nn_parameters_wizard import NNParametersWizard

class NNParametersDialog(QDialog):

    def __init__(self,parent=None):
        super().__init__(parent = parent)
        
        self.nn_parameters_wizard = NNParametersWizard()
        
        self.title = 'Non newtonian parameters'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        if self.nn_parameters_wizard.gencase_output_xml_exists == True:
        
            if self.nn_parameters_wizard.gencase_mkfluid_exists == True:
        
                self.fluid_phases_num = int(self.nn_parameters_wizard.gencase_mkfluid)
            
                self.rheology_options_tab = RheologyOptionsTab()
                self.set_rheology_options_tab()
                
                self.nn_parameters_tabwidget = QTabWidget()
                self.nn_parameters_tabwidget.addTab(self.rheology_options_tab,"Execution")
                
                self.phases_parameters_tab_list = []
                for current_phase in range(self.fluid_phases_num):
                    self.phases_parameters_tab_list.append(PhaseParametersTab())
                    self.set_phase_parameters_tab_entries(current_phase)
                    self.nn_parameters_tabwidget.addTab(self.phases_parameters_tab_list[current_phase],"Phase "+str(current_phase+1))
                
                ok_button = QPushButton('OK')
                ok_button.clicked.connect(self.launch_nn_parameters_wizard)
                ok_button.setToolTip('Apply change to XML (no need to run GenCase)')
                reset_button = QPushButton('Reset')
                reset_button.clicked.connect(self.set_default_parameters)
                reset_button.setToolTip('Reset default settings')
                cancel_button = QPushButton('Cancel')
                cancel_button.clicked.connect(self.close)
                cancel_button.setToolTip('Discard any unapplied change')
                
                self.layout = QGridLayout(self)
                self.layout.addWidget(self.nn_parameters_tabwidget,0,0,1,3)
                self.layout.addWidget(ok_button,1,0,1,1)
                self.layout.addWidget(reset_button,1,1,1,1)
                self.layout.addWidget(cancel_button,1,2,1,1)
                self.setLayout(self.layout)
                
                self.setMinimumWidth(400)
                self.center() 
                
                if not self.nn_parameters_wizard.nn_options_xml_exists:
                    warning_dialog('File nn_options.xml not found. Default settings applied')
                    
                self.exec_()
            else:
                warning_dialog('First add fluid particles and run GenCase')
        else:
            warning_dialog('Need to run GenCase before setting non netonian parameters')
       
    def set_phase_parameters_tab_entries(self,current_phase):
        if self.nn_parameters_wizard.nn_options_xml_exists:
            params = self.nn_parameters_wizard.parse_nn_parameters_xml_tree(current_phase)
            self.phases_parameters_tab_list[current_phase].phase_density.setText(params[0])
            self.phases_parameters_tab_list[current_phase].phase_kinematic_viscosity.setText(params[1])
            self.phases_parameters_tab_list[current_phase].phase_specific_yield_stress.setText(params[2])  
            self.phases_parameters_tab_list[current_phase].phase_max_yield_stress.setText(params[3])  
            self.phases_parameters_tab_list[current_phase].phase_max_yield_stress_multiplier.setText(params[4])  
            self.phases_parameters_tab_list[current_phase].phase_HBP_m_coefficient.setText(params[5])
            self.phases_parameters_tab_list[current_phase].phase_HBP_n_coefficient.setText(params[6]) 
            self.phases_parameters_tab_list[current_phase].phase_type.setCurrentIndex(int(params[7]))
            self.phases_parameters_tab_list[current_phase].indexChange()
        else:
            self.phases_parameters_tab_list[current_phase].default()
            
    def set_rheology_options_tab(self):
        if self.nn_parameters_wizard.nn_options_xml_exists:
            params = self.nn_parameters_wizard.parse_nn_parameters_xml_tree(100)
            self.rheology_options_tab.rheology_formulation_combobox.setCurrentIndex(int(params[0])-1)
            self.rheology_options_tab.velocity_gradient_formulation_combobox.setCurrentIndex(int(params[1])-1)
        pass
            
    def launch_nn_parameters_wizard(self):
        self.nn_parameters_wizard.set_nn_parameters(self.fluid_phases_num,self.rheology_options_tab,self.phases_parameters_tab_list)
        self.close()
            
    def set_default_parameters(self):
        self.rheology_options_tab.rheology_formulation_combobox.setCurrentIndex(1)
        self.rheology_options_tab.velocity_gradient_formulation_combobox.setCurrentIndex(0)
        for current_phase in range(self.fluid_phases_num):
            self.phases_parameters_tab_list[current_phase].default()
            
    # def closeEvent(self,event):
        # QApplication.quit() 
    
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class RheologyOptionsTab(QWidget):
    
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        
        self.rheology_formulation_combobox = QComboBox()
        self.rheology_formulation_combobox.addItem('Single-phase classic')
        self.rheology_formulation_combobox.addItem('Single and multi-phase')
        self.rheology_formulation_combobox.setToolTip('Rheology formulation 1:Single-phase classic, 2: Single and multi-phase')
        self.rheology_formulation_combobox.setCurrentIndex(1)
        self.velocity_gradient_formulation_combobox = QComboBox()
        self.velocity_gradient_formulation_combobox.addItem('FDA')
        self.velocity_gradient_formulation_combobox.addItem('SPH')
        self.velocity_gradient_formulation_combobox.setToolTip('Velocity gradient formulation 1:FDA, 2:SPH')
        
        self.layout.addWidget(QLabel('Rheology Treatment:'),0,0,1,1)
        self.layout.addWidget(QLabel('Velocity Gradient Type:'),1,0,1,1)
        self.layout.addWidget(self.rheology_formulation_combobox,0,1,1,1)
        self.layout.addWidget(self.velocity_gradient_formulation_combobox,1,1,1,1)
        self.setLayout(self.layout)
        
class PhaseParametersTab(QWidget):
    
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        
        self.phase_type = QComboBox()
        self.phase_type.addItem('Non newtonian')
        #self.phase_type.addItem('Newtonian')
        self.phase_density = QLineEdit()
        self.phase_kinematic_viscosity = QLineEdit()
        self.phase_specific_yield_stress = QLineEdit()       
        self.phase_max_yield_stress = QLineEdit()       
        self.phase_max_yield_stress_multiplier = QLineEdit()       
        self.phase_HBP_m_coefficient = QLineEdit()
        self.phase_HBP_n_coefficient = QLineEdit()
        
        self.phase_type.currentIndexChanged.connect(self.indexChange)
        
        self.phase_density.setToolTip('Density of the phase')
        self.phase_kinematic_viscosity.setToolTip('Kinematic viscosity (or consistency index) value for phase (m2/s)')
        self.phase_specific_yield_stress.setToolTip('Specific yield stress of phase (Pa m3/kg)')
        self.phase_max_yield_stress.setToolTip('User defined maximum specific yield stress of phase (Pa m3/kg)')
        self.phase_max_yield_stress_multiplier.setToolTip('tau_max multiplier for use with Bingham model or bi-viscosity model(tau_bi=tau_max*Bi_multi)')
        self.phase_HBP_m_coefficient.setToolTip('Use 0 to reduce Newtonian liquid, order of 10 for power law and order of 100 for Bingham (sec)')
        self.phase_HBP_n_coefficient.setToolTip('Use 1 to reduce to Newtonian, &lt;1 for shear thinning &gt;1 for shear thickenning')
        
        self.layout.addWidget(QLabel('Phase type: '),0,0,1,1)
        self.layout.addWidget(QLabel('Density: '),1,0,1,1) 
        self.layout.addWidget(QLabel('Kinematic viscosity: '),2,0,1,1) 
        self.layout.addWidget(QLabel('Specific yield stress: '),3,0,1,1)
        self.layout.addWidget(QLabel('Maximum yield stress: '),4,0,1,1)
        self.layout.addWidget(QLabel('Max.stress multiplier : '),5,0,1,1) 
        self.layout.addWidget(QLabel('HBP m index: '),6,0,1,1) 
        self.layout.addWidget(QLabel('HBP n index: '),7,0,1,1) 
        self.layout.addWidget(self.phase_type,0,1,1,1) 
        self.layout.addWidget(self.phase_density,1,1,1,1) 
        self.layout.addWidget(self.phase_kinematic_viscosity,2,1,1,1) 
        self.layout.addWidget(self.phase_specific_yield_stress,3,1,1,1) 
        self.layout.addWidget(self.phase_max_yield_stress,4,1,1,1) 
        self.layout.addWidget(self.phase_max_yield_stress_multiplier,5,1,1,1) 
        self.layout.addWidget(self.phase_HBP_m_coefficient,6,1,1,1) 
        self.layout.addWidget(self.phase_HBP_n_coefficient,7,1,1,1) 
        
        self.layout.setColumnStretch(0,1) 
        self.layout.setColumnStretch(1,1) 
        self.setLayout(self.layout)
    
    def default(self):
        self.phase_density.setText('1000')
        self.phase_kinematic_viscosity.setText('0.001')
        self.phase_specific_yield_stress.setText('0.001') 
        self.phase_max_yield_stress.setText('0.0015') 
        self.phase_max_yield_stress_multiplier.setText('10') 
        self.phase_HBP_m_coefficient.setText('100')
        self.phase_HBP_n_coefficient.setText('1') 
        self.phase_type.setCurrentIndex(0)
    
    def indexChange(self):
        if self.phase_type.currentIndex() == 0:
            self.index = False
        else:
            self.index = True    
        self.phase_density.setDisabled(self.index)
        self.phase_kinematic_viscosity.setDisabled(self.index)
        self.phase_specific_yield_stress.setDisabled(self.index)
        self.phase_max_yield_stress.setDisabled(self.index)
        self.phase_max_yield_stress_multiplier.setDisabled(self.index)
        self.phase_HBP_m_coefficient.setDisabled(self.index)
        self.phase_HBP_n_coefficient.setDisabled(self.index)