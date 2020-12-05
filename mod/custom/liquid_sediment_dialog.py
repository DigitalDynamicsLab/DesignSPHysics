#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Liquid-Sediment Parameters Dialog """

from PySide import QtGui

from mod import file_tools
from mod.dataobjects.case import Case
from mod.dialog_tools import warning_dialog

from mod.custom.lsparam import LsDict

class LiquidSedimentParametersDialog(QtGui.QDialog):

    def __init__(self,parent=None):
        super().__init__(parent = parent)
        
        self.title = 'Liquid-Sediment parameters'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        if Case.the().info.is_gencase_done:
            
            self.fluid_phases_num = len(Case.the().get_all_fluid_objects())
            
            if self.fluid_phases_num == 2:
            
                self.execution_options_tab = ExecutionOptionsTab()
                
                self.liquidsediment_parameters_tabwidget = QtGui.QTabWidget()
                self.liquidsediment_parameters_tabwidget.addTab(self.execution_options_tab,"Execution")
                
                self.phases_parameters_tab_list = []
                for current_phase in range(self.fluid_phases_num):
                    self.phases_parameters_tab_list.append(PhaseParametersTab())
                    self.set_phase_parameters_tab_entries(current_phase)
                    self.liquidsediment_parameters_tabwidget.addTab(self.phases_parameters_tab_list[current_phase],"Phase "+str(current_phase+1))
                
                apply_button = QtGui.QPushButton('Apply')
                apply_button.clicked.connect(self.on_apply_button)
                apply_button.setToolTip('Save current settings')
                reset_button = QtGui.QPushButton('Reset')
                reset_button.clicked.connect(self.set_default_parameters)
                reset_button.setToolTip('Reset default settings')
                cancel_button = QtGui.QPushButton('Cancel')
                cancel_button.clicked.connect(self.close)
                cancel_button.setToolTip('Discard any unapplied change')
                
                self.layout = QtGui.QGridLayout(self)
                self.layout.addWidget(self.liquidsediment_parameters_tabwidget,0,0,1,3)
                self.layout.addWidget(apply_button,1,0,1,1)
                self.layout.addWidget(reset_button,1,1,1,1)
                self.layout.addWidget(cancel_button,1,2,1,1)
                self.setLayout(self.layout)
                
                self.setMinimumWidth(400)
                self.center() 
                                    
                self.exec_()
            else:
                warning_dialog('Liquid-Sediment simulations requires necessarly 2 fluid phases')
        else:
            warning_dialog('Need to run GenCase before setting liquid-sediment parameters')
    
    def on_apply_button(self):
        for current_phase in range(self.fluid_phases_num):
            current_phase_dict = Case.the().lsparam.tabs_list[current_phase]
            Case.the().lsparam.eps = self.execution_options_tab.eps_coefficient.text()
            Case.the().lsparam.deltasph = self.execution_options_tab.deltasph_coefficient.text()
            Case.the().lsparam.tabs_list[current_phase]['mk'] = self.phases_parameters_tab_list[current_phase].phase_mk.text()
            Case.the().lsparam.tabs_list[current_phase]['density'] = self.phases_parameters_tab_list[current_phase].phase_density.text()
            Case.the().lsparam.tabs_list[current_phase]['csound'] = self.phases_parameters_tab_list[current_phase].phase_csound.text()
            Case.the().lsparam.tabs_list[current_phase]['gamma'] = self.phases_parameters_tab_list[current_phase].phase_gamma.text()
            Case.the().lsparam.tabs_list[current_phase]['viscosity'] = self.phases_parameters_tab_list[current_phase].phase_viscosity.text()
            Case.the().lsparam.tabs_list[current_phase]['HBP_n'] = self.phases_parameters_tab_list[current_phase].phase_HBP_n_coefficient.text()
            Case.the().lsparam.tabs_list[current_phase]['HBP_m'] = self.phases_parameters_tab_list[current_phase].phase_HBP_m_coefficient.text()
            Case.the().lsparam.tabs_list[current_phase]['cohesion'] = self.phases_parameters_tab_list[current_phase].phase_cohesion.text()
            Case.the().lsparam.tabs_list[current_phase]['reposeangle'] = self.phases_parameters_tab_list[current_phase].phase_reposeangle.text()
            Case.the().lsparam.tabs_list[current_phase]['constantyield'] = self.phases_parameters_tab_list[current_phase].phase_constantyield.text()
            Case.the().lsparam.tabs_list[current_phase]['phase_type'] = str(self.phases_parameters_tab_list[current_phase].phase_type.currentIndex())
            
            # warning_dialog('Saving phase: ' + str(current_phase + 1) +'\n' + 'Number of phase dicts: ' + str(len(Case.the().lsparam.tabs_list)) + '\n'
            # + str(Case.the().lsparam.tabs_list[current_phase]))
            
        file_tools.save_case(Case.the().path,Case.the())
        
        Case.the().info.liquidsediment_phase_list_exists = True
        
        self.close()
    
    def set_phase_parameters_tab_entries(self,current_phase):  
            
        if not len(Case.the().lsparam.tabs_list) > current_phase:
            Case.the().lsparam.tabs_list.append(LsDict().phase_dict)
            Case.the().lsparam.tabs_list[current_phase]['mk'] = str(current_phase)
            
        self.phases_parameters_tab_list[current_phase].phase_mk.setText(Case.the().lsparam.tabs_list[current_phase]['mk'])
        self.phases_parameters_tab_list[current_phase].phase_density.setText(Case.the().lsparam.tabs_list[current_phase]['density'])
        self.phases_parameters_tab_list[current_phase].phase_csound.setText(Case.the().lsparam.tabs_list[current_phase]['csound'])
        self.phases_parameters_tab_list[current_phase].phase_gamma.setText(Case.the().lsparam.tabs_list[current_phase]['gamma'])
        self.phases_parameters_tab_list[current_phase].phase_viscosity.setText(Case.the().lsparam.tabs_list[current_phase]['viscosity'])
        self.phases_parameters_tab_list[current_phase].phase_HBP_n_coefficient.setText(Case.the().lsparam.tabs_list[current_phase]['HBP_n']) 
        self.phases_parameters_tab_list[current_phase].phase_HBP_m_coefficient.setText(Case.the().lsparam.tabs_list[current_phase]['HBP_m'])
        self.phases_parameters_tab_list[current_phase].phase_cohesion.setText(Case.the().lsparam.tabs_list[current_phase]['cohesion']) 
        self.phases_parameters_tab_list[current_phase].phase_reposeangle.setText(Case.the().lsparam.tabs_list[current_phase]['reposeangle']) 
        self.phases_parameters_tab_list[current_phase].phase_constantyield.setText(Case.the().lsparam.tabs_list[current_phase]['constantyield']) 
        self.phases_parameters_tab_list[current_phase].phase_type.setCurrentIndex(int(Case.the().lsparam.tabs_list[current_phase]['phase_type']))
        self.phases_parameters_tab_list[current_phase].indexChange()
        
        # warning_dialog('Setting phase: ' + str(current_phase + 1) +'\n' + 'Number of phase dicts: ' + str(len(Case.the().lsparam.tabs_list)) + '\n'
            # + str(Case.the().lsparam.tabs_list[current_phase]) + '\n')
    
    def set_default_parameters(self):
        self.execution_options_tab.eps_coefficient.setText('0.0')
        self.execution_options_tab.deltasph_coefficient.setText('0.1')
        for current_phase in range(self.fluid_phases_num):
            self.phases_parameters_tab_list[current_phase].default(str(current_phase))
            
    # def closeEvent(self,event):
        # QtGui.QApplication.quit() 
    
    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class ExecutionOptionsTab(QtGui.QWidget):
    
    def __init__(self):
        super().__init__()
        self.layout = QtGui.QGridLayout()
        
        self.eps_coefficient = QtGui.QLineEdit(Case.the().lsparam.eps)
        self.deltasph_coefficient = QtGui.QLineEdit(Case.the().lsparam.deltasph)
        
        self.layout.addWidget(QtGui.QLabel('Eps coefficient:'),0,0,1,1)
        self.layout.addWidget(QtGui.QLabel('DeltaSPH coefficient:'),1,0,1,1)
        self.layout.addWidget(self.eps_coefficient,0,1,1,1)
        self.layout.addWidget(self.deltasph_coefficient,1,1,1,1)
        self.setLayout(self.layout)
        
class PhaseParametersTab(QtGui.QWidget):
    
    def __init__(self):
        super().__init__()
        self.layout = QtGui.QGridLayout()
        
        self.phase_type = QtGui.QComboBox()
        self.phase_type.addItem('Non newtonian')
        self.phase_type.addItem('Newtonian')
        
        self.phase_mk = QtGui.QLineEdit()
        self.phase_density = QtGui.QLineEdit()
        self.phase_csound = QtGui.QLineEdit()
        self.phase_gamma = QtGui.QLineEdit()
        self.phase_viscosity = QtGui.QLineEdit()
        self.phase_HBP_n_coefficient = QtGui.QLineEdit()
        self.phase_HBP_m_coefficient = QtGui.QLineEdit()
        self.phase_cohesion = QtGui.QLineEdit()
        self.phase_reposeangle = QtGui.QLineEdit()
        self.phase_constantyield = QtGui.QLineEdit()
        
        self.phase_type.currentIndexChanged.connect(self.indexChange)
        
        self.phase_mk.setToolTip('Mkfluid of the phase')
        self.phase_density.setToolTip('Density of the phase (kg/m^3)')
        self.phase_csound.setToolTip('Sound coefficient of the phase')
        self.phase_gamma.setToolTip('Polytropic coefficient of the phase')
        self.phase_viscosity.setToolTip('Viscosity value for phase (m^2/s)')
        self.phase_HBP_n_coefficient.setToolTip('Use 1 to reduce to Newtonian, &lt;1 for shear thinning &gt;1 for shear thickenning')
        self.phase_HBP_m_coefficient.setToolTip('Use 0 to reduce Newtonian liquid, order of 10 for power law and order of 100 for Bingham (sec)')
        self.phase_cohesion.setToolTip('Shear strength of the phase (kPa)')
        self.phase_reposeangle.setToolTip('Internal friction angle of the phase (deg)')
        self.phase_constantyield.setToolTip('Constant yield stress of the phase, used if > 0 (Pa?)')
        
        self.label_layout = QtGui.QVBoxLayout()
        self.label_layout.addWidget(QtGui.QLabel('Phase type: '))
        self.label_layout.addWidget(QtGui.QLabel('Phase mkfluid: ')) 
        self.label_layout.addWidget(QtGui.QLabel('Density: ')) 
        self.label_layout.addWidget(QtGui.QLabel('Sound coefficient: ')) 
        self.label_layout.addWidget(QtGui.QLabel('Polytropic coefficient: ')) 
        self.label_layout.addWidget(QtGui.QLabel('Viscosity: ')) 
        self.label_layout.addWidget(QtGui.QLabel('HBP n index: '))
        self.label_layout.addWidget(QtGui.QLabel('HBP m index: ')) 
        self.label_layout.addWidget(QtGui.QLabel('Shear strength: '))
        self.label_layout.addWidget(QtGui.QLabel('Internal friction angle: '))
        self.label_layout.addWidget(QtGui.QLabel('Constant yield stress: '))
        
        self.lineedit_layout = QtGui.QVBoxLayout()
        self.lineedit_layout.addWidget(self.phase_type) 
        self.lineedit_layout.addWidget(self.phase_mk) 
        self.lineedit_layout.addWidget(self.phase_density) 
        self.lineedit_layout.addWidget(self.phase_csound) 
        self.lineedit_layout.addWidget(self.phase_gamma) 
        self.lineedit_layout.addWidget(self.phase_viscosity) 
        self.lineedit_layout.addWidget(self.phase_HBP_n_coefficient) 
        self.lineedit_layout.addWidget(self.phase_HBP_m_coefficient) 
        self.lineedit_layout.addWidget(self.phase_cohesion) 
        self.lineedit_layout.addWidget(self.phase_reposeangle) 
        self.lineedit_layout.addWidget(self.phase_constantyield) 
        
        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.addLayout(self.label_layout)
        self.main_layout.addLayout(self.lineedit_layout)
        
        self.setLayout(self.main_layout)
    
    def default(self,phasenum):
        self.phase_mk.setText(phasenum)
        self.phase_density.setText('1500')
        self.phase_csound.setText('20')
        self.phase_gamma.setText('7')
        self.phase_viscosity.setText('0.001')
        self.phase_HBP_n_coefficient.setText('1')
        self.phase_HBP_m_coefficient.setText('100')
        self.phase_cohesion.setText('1.0')
        self.phase_reposeangle.setText('35')
        self.phase_constantyield.setText('0')
        self.phase_type.setCurrentIndex(0)
    
    def indexChange(self):
        if self.phase_type.currentIndex() == 0:
            self.index = False
        else:
            self.index = True    
        self.phase_HBP_n_coefficient.setDisabled(self.index)
        self.phase_HBP_m_coefficient.setDisabled(self.index)
        self.phase_cohesion.setDisabled(self.index)
        self.phase_reposeangle.setDisabled(self.index)
        self.phase_constantyield.setDisabled(self.index)
