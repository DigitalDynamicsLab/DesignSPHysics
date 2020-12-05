#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Liquid Sediment Parameters Wizard """

import os
import xml.etree.ElementTree as etree
from xml.dom import minidom
from xml.dom.minidom import Node

from mod.dataobjects.case import Case
from mod.dialog_tools import warning_dialog

class LiquidSedimentXMLWizard:
    
    def __init__(self,parent=None):
        
        self.phase_count = len(Case.the().get_all_fluid_objects())
        
        gencase_output_xml_path = Case.the().get_out_xml_file_path() + '.xml'
        execution_template_xml_path = r"C:\Users\penzo\AppData\Roaming\FreeCAD\Mod\DesignSPHysics\mod\custom\lstmp_execution.xml"
        phase_template_xml_path = r"C:\Users\penzo\AppData\Roaming\FreeCAD\Mod\DesignSPHysics\mod\custom\lstmp_phase.xml"
        
        self.gencase_output_xml_exists = False
        if os.path.exists(gencase_output_xml_path):          
            self.gencase_output_xml_exists = True 
            
            ### removing that strange header ###
            from_file = open(gencase_output_xml_path,mode="r") 
            header = from_file.readline()        
            if header.find("<!--") >= 0:
                gencase_xml_tree = etree.parse(from_file)
            else:
                gencase_xml_tree = etree.parse(gencase_output_xml_path)
            
            ### removing default parameters ###
            self.liquidsediment_xml_root = gencase_xml_tree.getroot()
            if self.liquidsediment_xml_root is not None:        
                default_parameters =  self.liquidsediment_xml_root.find('.//execution/parameters')
                for parameter in default_parameters.findall('parameter'):
                    default_parameters.remove(parameter)
            
            ### reading templates ###
            self.execution_template_xml_root = etree.parse(execution_template_xml_path).getroot()
            self.phase_template_xml_root = etree.parse(phase_template_xml_path).getroot()
            
            self.update_output_xml(gencase_output_xml_path)
            
    def update_output_xml(self,gencase_output_xml_path):        
            
        liquidsediment_xml_tree = etree.ElementTree(self.liquidsediment_xml_root)
        
        for current_phase in range(self.phase_count):
            phase_root = PhaseRoot()
            for child in phase_root.root.iter('parameter'):
                child.attrib['key'] = child.attrib['key'].replace('XXX',str(current_phase))
            param = 0
            for child in phase_root.root.iter('parameter'):
                child.attrib['value'] = child.attrib['value'].replace('YYY',list(Case.the().lsparam.tabs_list[current_phase].values())[param])
                param += 1
            for child in phase_root.root.iter('parameter'):
                liquidsediment_xml_tree.find('.//execution/parameters').append(etree.Element(child.tag,child.attrib))
            
        for child in self.execution_template_xml_root.iter('parameter'):
            liquidsediment_xml_tree.find('.//execution/parameters').append(etree.Element(child.tag,child.attrib))
        
        eps = self.execution_template_xml_root.find('eps')   
        liquidsediment_xml_tree.find('.//casedef/constantsdef').append(etree.Element(eps.tag,eps.attrib))        
        liquidsediment_xml_tree.find(".//casedef/constantsdef/eps").attrib['value'] = Case.the().lsparam.eps
        
        liquidsediment_xml_tree.find(".//execution/parameters/parameter[@key='DeltaSPH']").attrib['value'] = Case.the().lsparam.deltasph
        liquidsediment_xml_tree.find(".//execution/parameters/parameter[@key='DtIni']").attrib['value'] = str(Case.the().execution_parameters.dtini)
        liquidsediment_xml_tree.find(".//execution/parameters/parameter[@key='DtMin']").attrib['value'] = str(Case.the().execution_parameters.dtmin)
        liquidsediment_xml_tree.find(".//execution/parameters/parameter[@key='TimeMax']").attrib['value'] = str(Case.the().execution_parameters.timemax)
        liquidsediment_xml_tree.find(".//execution/parameters/parameter[@key='TimeOut']").attrib['value'] = str(Case.the().execution_parameters.timeout)
        liquidsediment_xml_tree.find(".//execution/parameters/parameter[@key='IncZ']").attrib['value'] = '0'
        liquidsediment_xml_tree.find(".//execution/parameters/parameter[@key='PartsOutMax']").attrib['value'] = str(Case.the().execution_parameters.partsoutmax)
        liquidsediment_xml_tree.find(".//execution/parameters/parameter[@key='PhaseCount']").attrib['value'] = str(self.phase_count)
        
        posmin = liquidsediment_xml_tree.find(".//execution/particles/_summary/positions/posmin")
        if Case.the().domain.posmin_x.type == 1:
            posmin.attrib['x'] = str(Case.the().domain.posmin_x.value)
        if Case.the().domain.posmin_y.type == 1:
            posmin.attrib['y'] = str(Case.the().domain.posmin_y.value)
        if Case.the().domain.posmin_z.type == 1:
            posmin.attrib['z'] = str(Case.the().domain.posmin_z.value)

        posmax = liquidsediment_xml_tree.find(".//execution/particles/_summary/positions/posmax")
        if Case.the().domain.posmax_x.type == 1:
            posmax.attrib['x'] = str(Case.the().domain.posmax_x.value)
        if Case.the().domain.posmax_y.type == 1:
            posmax.attrib['y'] = str(Case.the().domain.posmax_y.value)
        if Case.the().domain.posmax_z.type == 1:
            posmax.attrib['z'] = str(Case.the().domain.posmax_z.value)
        
        self.write_output_xml(liquidsediment_xml_tree,gencase_output_xml_path)
        
    def write_output_xml(self,liquidsediment_xml_tree,file_path):
        liquidsediment_xml_tree.write(file_path)
        xml_file = minidom.parse(file_path)
        self.remove_blanks_in_output_xml(xml_file)
        xml_file.normalize()
        f = open(file_path, 'w')
        f.write(xml_file.toprettyxml(indent = "\t"))
        f.close()

    def remove_blanks_in_output_xml(self,node):    
        for x in node.childNodes:
            if x.nodeType == Node.TEXT_NODE:
                if x.nodeValue:
                    x.nodeValue = x.nodeValue.strip()
            elif x.nodeType == Node.ELEMENT_NODE:
                self.remove_blanks_in_output_xml(x)
                
class PhaseRoot():
    
    def __init__(self):
        phase_template_xml_path = r"C:\Users\penzo\AppData\Roaming\FreeCAD\Mod\DesignSPHysics\mod\custom\lstmp_phase.xml"
        self.root = etree.parse(phase_template_xml_path).getroot()
        