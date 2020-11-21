#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Non Newtonian Parameters Wizard """

import os
import xml.etree.ElementTree as etree
from xml.dom import minidom
from xml.dom.minidom import Node

from mod.dataobjects.case import Case

class NNParametersWizard():
    
    def __init__(self):
    
        self.case_name = Case.the().path.split('/')[-1]
        self.gencase_output_xml_path = Case.the().path+'/'+self.case_name+'_out/'+self.case_name+'.xml' 
        self.dirin = Case.the().path+'/'+self.case_name+'_out'    
        
        self.nn_options_xml_exists = False
        self.nn_options_xml_name = 'nn_options.xml'
        self.nn_options_xml_path = self.dirin+'/'+self.nn_options_xml_name
        
        if os.path.exists(self.nn_options_xml_path):
            os.chdir(self.dirin) 
            self.nn_options_xml_exists = True  
            self.nn_options_xml_tree = etree.parse(self.nn_options_xml_path)   
            self.nn_options_xml_root = self.nn_options_xml_tree.getroot()
            
        self.gencase_output_xml_exists = False
        if os.path.exists(self.gencase_output_xml_path):
            self.gencase_output_xml_exists = True 
            
            ### removing that strange header ###
            from_file = open(self.gencase_output_xml_path,mode="r") 
            header = from_file.readline()        
            if header.find("<!--") >= 0:
                self.gencase_xml_tree = etree.parse(from_file)
            else:
                self.gencase_xml_tree = etree.parse(self.gencase_output_xml_path)
             
            self.gencase_xml_root = self.gencase_xml_tree.getroot()
            if self.gencase_xml_root is not None:
                self.gencase_mkfluid_exists = True
                try:
                    self.gencase_mkfluid = self.gencase_xml_root.findall(".//execution/particles/_summary/fluid")[0].attrib['mkcount']
                except:
                    self.gencase_mkfluid_exists = False
                self.gencase_xml_nn_parameters_exist = False
                # if len(self.gencase_xml_root.findall(".//execution/special")[0].getchildren()) > 0:
                    # self.gencase_xml_nn_parameters_exist = True 
                gencase_special = self.gencase_xml_root.findall(".//execution/special")[0]
                for elem in gencase_special.iter():
                    if elem.tag == 'phase':
                        self.gencase_xml_nn_parameters_exist = True
                        break                
                if self.gencase_xml_nn_parameters_exist == False:
                    self.recover_bad_parameters()
    
    def recover_bad_parameters(self):
        self.gencase_xml_root.findall(".//execution/parameters/parameter[@key='#DtIni']")[0].attrib['key'] = 'DtIni'
        self.gencase_xml_root.findall(".//execution/parameters/parameter[@key='#DtMin']")[0].attrib['key'] = 'DtMin'
            
    def set_nn_parameters(self,phaseNum,rheTab,phaseTabs):
        if self.gencase_xml_nn_parameters_exist == False:
            #self.recover_bad_parameters()
            self.gencase_xml_root.findall('.//execution/parameters')[0].append(
                etree.Element('parameter',
                              {'key':'RheologyTreatment',
                              'value':str(rheTab.rheology_formulation_combobox.currentIndex()+1),
                              'comment':'Rheology formulation 1:Single-phase classic, 2: Single and multi-phase'
                              }))
            self.gencase_xml_root.findall('.//execution/parameters')[0].append(
                etree.Element('parameter',
                              {'key':'VelocityGradientType',
                              'value':str(rheTab.velocity_gradient_formulation_combobox.currentIndex()+1),
                              'comment':'Velocity gradient formulation 1:FDA, 2:SPH'
                              }))
            self.gencase_xml_root.findall('.//execution/special')[0].append(etree.Element('nnphases'))
            for curr_phase in range(phaseNum):               
                 self.gencase_xml_root.findall('.//execution/special/nnphases')[0].append(
                     etree.Element('phase',
                                   {'mkfluid':str(curr_phase)})) 
                 phase_parameters = [
                     ['rhop',{'value':phaseTabs[curr_phase].phase_density.text(),'comment':'Density of the phase'}],
                     ['visco',{'value':phaseTabs[curr_phase].phase_kinematic_viscosity.text(),'comment':'Kinematic viscosity (or consistency index) value for phase (m2/s)'}],
                     ['tau_yield',{'value':phaseTabs[curr_phase].phase_specific_yield_stress.text(),'comment':'Specific yield stress of phase (Pa m3/kg)'}],
                     ['tau_max',{'value':phaseTabs[curr_phase].phase_specific_yield_stress.text(),'comment':'User defined maximum specific yield stress of phase (Pa m3/kg)'}],
                     ['Bi_multi',{'value':phaseTabs[curr_phase].phase_specific_yield_stress.text(),'comment':'tau_max multiplier for use with Bingham model or bi-viscosity model(tau_bi=tau_max*Bi_multi)'}],
                     ['HBP_m',{'value':phaseTabs[curr_phase].phase_HBP_m_coefficient.text(),'comment':'Use 0 to reduce Newtonian liquid, order of 10 for power law and order of 100 for Bingham (sec)'}],
                     ['HBP_n',{'value':phaseTabs[curr_phase].phase_HBP_n_coefficient.text(),'comment':'Use 1 to reduce to Newtonian, <1 for shear thinning >1 for shear thickenning'}],
                     ['phasetype',{'value':str(phaseTabs[curr_phase].phase_type.currentIndex()),'comment':'Non-Newtonian=0 only option in beta'}]
                     ]
                 for param in phase_parameters:
                     self.gencase_xml_root.findall('.//execution/special/nnphases/phase')[curr_phase].append(
                         etree.Element(param[0],param[1]))
            self.gencase_xml_nn_parameters_exist = True
            
            self.init_nn_parameters_xml_tree(int(self.gencase_mkfluid))

        else:
            if self.nn_options_xml_exists == False:
                self.init_nn_parameters_xml_tree(int(self.gencase_mkfluid))
            self.gencase_xml_root.findall(".//execution/parameters/parameter[@key='RheologyTreatment']")[0].attrib['value'] = str(rheTab.rheology_formulation_combobox.currentIndex()+1) 
            self.gencase_xml_root.findall(".//execution/parameters/parameter[@key='VelocityGradientType']")[0].attrib['value'] = str(rheTab.velocity_gradient_formulation_combobox.currentIndex()+1)
            self.nn_options_xml_root.findall(".//parameter[@key='RheologyTreatment']")[0].attrib['value'] = str(rheTab.rheology_formulation_combobox.currentIndex()+1) 
            self.nn_options_xml_root.findall(".//parameter[@key='VelocityGradientType']")[0].attrib['value'] = str(rheTab.velocity_gradient_formulation_combobox.currentIndex()+1)
            for curr_phase in range(phaseNum):               
                phase_parameters = [
                    ['rhop',phaseTabs[curr_phase].phase_density.text()],
                    ['visco',phaseTabs[curr_phase].phase_kinematic_viscosity.text()],
                    ['tau_yield',phaseTabs[curr_phase].phase_specific_yield_stress.text()],
                    ['tau_max',phaseTabs[curr_phase].phase_max_yield_stress.text()],
                    ['Bi_multi',phaseTabs[curr_phase].phase_max_yield_stress_multiplier.text()],
                    ['HBP_m',phaseTabs[curr_phase].phase_HBP_m_coefficient.text()],
                    ['HBP_n',phaseTabs[curr_phase].phase_HBP_n_coefficient.text()],
                    ['phasetype',str(phaseTabs[curr_phase].phase_type.currentIndex())]
                    ]
                parent = self.gencase_xml_root.findall('.//execution/special/nnphases/phase')[curr_phase]
                parentSpecial = self.nn_options_xml_root.findall('.//special/nnphases/phase')[curr_phase]
                for param in phase_parameters:
                    parent.find(param[0]).attrib['value'] = param[1]
                    parentSpecial.find(param[0]).attrib['value'] = param[1]
            
        self.gencase_xml_root.findall(".//casedef/constantsdef/rhop0")[0].attrib['value'] = self.nn_options_xml_root.findall(".//special/nnphases/phase[@mkfluid='0']/rhop")[0].attrib['value']
        self.gencase_xml_root.findall(".//execution/constants/rhop0")[0].attrib['value'] = self.nn_options_xml_root.findall(".//special/nnphases/phase[@mkfluid='0']/rhop")[0].attrib['value']            
        self.prettify_output_xml(self.gencase_xml_tree,self.gencase_output_xml_path)
        self.prettify_output_xml(self.nn_options_xml_tree,self.nn_options_xml_path)
        #self.gencase_xml_tree.write(self.case_name)
        #self.nn_options_xml_tree.write(self.nn_options_xml_name)
    
    def prettify_output_xml(self,gencase_xml_tree,file_path):
        gencase_xml_tree.write(file_path)
        xml_file = minidom.parse(file_path)
        self.remove_blanks_in_output_xml(xml_file)
        xml_file.normalize()
        f = open(file_path, 'w')
        f.write(xml_file.toprettyxml(indent = '  '))
        f.close()

    def remove_blanks_in_output_xml(self,node):    
        for x in node.childNodes:
            if x.nodeType == Node.TEXT_NODE:
                if x.nodeValue:
                    x.nodeValue = x.nodeValue.strip()
            elif x.nodeType == Node.ELEMENT_NODE:
                self.remove_blanks_in_output_xml(x)
        
    def init_nn_parameters_xml_tree(self,phaseNum):
        if self.nn_options_xml_exists == True:
            os.remove(self.nn_options_xml_path)
        # else:
            # with open(self.nn_options_xml_path, 'w'): 
                # pass
        etree.ElementTree(etree.Element('nnparameters')).write(self.nn_options_xml_path)
        self.nn_options_xml_tree = etree.parse(self.nn_options_xml_path)   
        self.nn_options_xml_root = self.nn_options_xml_tree.getroot()
        phases= self.gencase_xml_root.findall('.//execution/special/nnphases/phase')
        rhe = self.gencase_xml_root.findall(".//execution/parameters/parameter[@key='RheologyTreatment']")[0]
        vel = self.gencase_xml_root.findall(".//execution/parameters/parameter[@key='VelocityGradientType']")[0]
        self.nn_options_xml_root.append(etree.Element('special'))
        self.nn_options_xml_root.findall('.//special')[0].append(etree.Element('nnphases'))
        for curr_phase in range(phaseNum):
            self.nn_options_xml_root.findall('.//special/nnphases')[0].append(etree.Element('phase',{'mkfluid':str(curr_phase)}))
            for elem in phases[curr_phase].iter():
                if elem.tag != 'phase':
                     self.nn_options_xml_root.findall('.//special/nnphases/phase')[curr_phase].append(
                         etree.Element(elem.tag,elem.attrib))
        self.nn_options_xml_root.append(etree.Element(rhe.tag,rhe.attrib))
        self.nn_options_xml_root.append(etree.Element(vel.tag,vel.attrib))
    
    def parse_nn_parameters_xml_tree(self,curr_phase):
        params = []
        if curr_phase == 100:
            params.append(self.nn_options_xml_root.findall(".//parameter[@key='RheologyTreatment']")[0].attrib['value'])
            params.append(self.nn_options_xml_root.findall(".//parameter[@key='VelocityGradientType']")[0].attrib['value'])
        else:
            phases = self.nn_options_xml_root.findall('.//special/nnphases/phase')[curr_phase]            
            for phase in phases.iter():
                if phase.tag != 'phase':
                    params.append(phase.attrib['value'])
        return params
    
    def update_nn_parameters(self,target_params = None):
        if self.gencase_xml_nn_parameters_exist == False:
            self.gencase_xml_root.findall('.//execution/parameters')[0].append(
                etree.Element('parameter',
                              {'key':'RheologyTreatment',
                              'value':'2',
                              'comment':'Rheology formulation 1:Single-phase classic, 2: Single and multi-phase'
                              }))
            self.gencase_xml_root.findall('.//execution/parameters')[0].append(
                etree.Element('parameter',
                              {'key':'VelocityGradientType',
                              'value':'1',
                              'comment':'Velocity gradient formulation 1:FDA, 2:SPH'
                              }))
            self.gencase_xml_root.findall('.//execution/special')[0].append(etree.Element('nnphases'))
            for curr_phase in range(int(self.gencase_mkfluid)):               
                 self.gencase_xml_root.findall('.//execution/special/nnphases')[0].append(
                     etree.Element('phase',
                                   {'mkfluid':str(curr_phase)})) 
                 phase_parameters = [
                     ['rhop',{'value':'1000','comment':'Density of the phase'}],
                     ['visco',{'value':'0.1','comment':'Kinematic viscosity (or consistency index) value for phase (m2/s)'}],
                     ['tau_yield',{'value':'0.001','comment':'Specific yield stress of phase (Pa m3/kg)'}],
                     ['tau_max',{'value':'0.0015','comment':'User defined maximum specific yield stress of phase (Pa m3/kg)'}],
                     ['Bi_multi',{'value':'10','comment':'tau_max multiplier for use with Bingham model or bi-viscosity model(tau_bi=tau_max*Bi_multi)'}],
                     ['HBP_m',{'value':'10','comment':'Use 0 to reduce Newtonian liquid, order of 10 for power law and order of 100 for Bingham (sec)'}],
                     ['HBP_n',{'value':'2','comment':'Use 1 to reduce to Newtonian, <1 for shear thinning >1 for shear thickenning'}],
                     ['phasetype',{'value':'0','comment':'Non-Newtonian=0 only option in beta'}]
                     ]
                 for param in phase_parameters:
                     self.gencase_xml_root.findall('.//execution/special/nnphases/phase')[curr_phase].append(
                         etree.Element(param[0],param[1]))
            self.gencase_xml_nn_parameters_exist = True
        
        if self.nn_options_xml_exists == False:
            self.init_nn_parameters_xml_tree(int(self.gencase_mkfluid))
            
        rheParams = self.parse_nn_parameters_xml_tree(100)
        self.gencase_xml_root.findall(".//execution/parameters/parameter[@key='RheologyTreatment']")[0].attrib['value'] = rheParams[0] 
        self.gencase_xml_root.findall(".//execution/parameters/parameter[@key='VelocityGradientType']")[0].attrib['value'] = rheParams[1]
        self.nn_options_xml_root.findall(".//parameter[@key='RheologyTreatment']")[0].attrib['value'] = rheParams[0] 
        self.nn_options_xml_root.findall(".//parameter[@key='VelocityGradientType']")[0].attrib['value'] = rheParams[1] 
        for curr_phase in range(int(self.gencase_mkfluid)): 
            params = self.parse_nn_parameters_xml_tree(curr_phase)
            phase_parameters = [
                ['rhop',params[0]],
                ['visco',params[1]],
                ['tau_yield',params[2]],
                ['tau_max',params[3]],
                ['Bi_multi',params[4]],
                ['HBP_m',params[5]],
                ['HBP_n',params[6]],
                ['phasetype',params[7]]
                ]
            if target_params is not None:
                for target in target_params:
                    for param in phase_parameters:
                        if target[0] in param:
                            param[1] = target[1]           
                    
            parent = self.gencase_xml_root.findall('.//execution/special/nnphases/phase')[curr_phase]
            parentSpecial = self.nn_options_xml_root.findall('.//special/nnphases/phase')[curr_phase]
            for param in phase_parameters:
                parent.find(param[0]).attrib['value'] = param[1]
                parentSpecial.find(param[0]).attrib['value'] = param[1]
                
        self.gencase_xml_root.findall(".//casedef/constantsdef/rhop0")[0].attrib['value'] = self.nn_options_xml_root.findall(".//special/nnphases/phase[@mkfluid='0']/rhop")[0].attrib['value']
        self.gencase_xml_root.findall(".//execution/constants/rhop0")[0].attrib['value'] = self.nn_options_xml_root.findall(".//special/nnphases/phase[@mkfluid='0']/rhop")[0].attrib['value'] 
        self.prettify_output_xml(self.gencase_xml_tree,self.gencase_output_xml_path)
        self.prettify_output_xml(self.nn_options_xml_tree,self.nn_options_xml_path)
        #self.gencase_xml_tree.write(self.case_name)
        #self.nn_options_xml_tree.write(self.nn_options_xml_name)