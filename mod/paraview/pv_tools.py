#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Paraview tools"""

from socket import *
import pickle
import os 
import subprocess

import FreeCAD

from PySide import QtGui

from mod.dialog_tools import info_dialog

from mod.dataobjects.case import Case
 
from mod import file_tools

class PvSettingsDialog(QtGui.QDialog):
    def __init__(self,parent = None):
        super().__init__(parent = parent)
        
        self.setWindowTitle("Default export options")
               
        self.boundaryfixed = QtGui.QLineEdit(Case.the().pvparam.params["boundaryfixed"])
        self.boundarymoving = QtGui.QLineEdit(Case.the().pvparam.params["boundarymoving"])
        self.isosurface = QtGui.QLineEdit(Case.the().pvparam.params["isosurface"])
        self.partall = QtGui.QLineEdit(Case.the().pvparam.params["partall"])
        self.partbound = QtGui.QLineEdit(Case.the().pvparam.params["partbound"])
        self.partfluid = QtGui.QLineEdit(Case.the().pvparam.params["partfluid"])
        self.partfixed = QtGui.QLineEdit(Case.the().pvparam.params["partfixed"])
        self.partmoving = QtGui.QLineEdit(Case.the().pvparam.params["partmoving"])
        self.partfloating = QtGui.QLineEdit(Case.the().pvparam.params["partfloating"])
        self.forces = QtGui.QLineEdit(Case.the().pvparam.params["forces"])
        
        label_layout = QtGui.QVBoxLayout()
        label_layout.addWidget(QtGui.QLabel("BoundaryVTK - Fixed:"))
        label_layout.addWidget(QtGui.QLabel("BoundaryVTK - Moving:"))
        label_layout.addWidget(QtGui.QLabel("IsoSurface:"))
        label_layout.addWidget(QtGui.QLabel("PartVTK - All:"))
        label_layout.addWidget(QtGui.QLabel("PartVTK - Bound:"))
        label_layout.addWidget(QtGui.QLabel("PartVTK - Fluid:"))
        label_layout.addWidget(QtGui.QLabel("PartVTK - Fixed:"))
        label_layout.addWidget(QtGui.QLabel("PartVTK - Moving:"))
        label_layout.addWidget(QtGui.QLabel("PartVTK - Floating"))
        label_layout.addWidget(QtGui.QLabel("ComputeForces:"))
        lineedit_layout = QtGui.QVBoxLayout()
        lineedit_layout.addWidget(self.boundaryfixed)
        lineedit_layout.addWidget(self.boundarymoving)
        lineedit_layout.addWidget(self.isosurface)
        lineedit_layout.addWidget(self.partall)
        lineedit_layout.addWidget(self.partbound)
        lineedit_layout.addWidget(self.partfixed)
        lineedit_layout.addWidget(self.partfluid)
        lineedit_layout.addWidget(self.partmoving)
        lineedit_layout.addWidget(self.partfloating)
        lineedit_layout.addWidget(self.forces)
        
        layout = QtGui.QHBoxLayout()
        layout.addLayout(label_layout)
        layout.addLayout(lineedit_layout)
        self.groupbox = QtGui.QGroupBox("Default save name") 
        self.groupbox.setLayout(layout)    
        
        self.apply_button = QtGui.QPushButton("Apply")
        self.apply_button.clicked.connect(self.on_apply_button)
        
        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.addWidget(self.groupbox)
        self.main_layout.addWidget(self.apply_button)
        
        self.setLayout(self.main_layout)
        
        self.show()
        
    def on_apply_button(self):
        Case.the().pvparam.params["boundaryfixed"] = self.boundaryfixed.text()
        Case.the().pvparam.params["boundarymoving"] = self.boundarymoving.text()
        Case.the().pvparam.params["isosurface"] = self.isosurface.text()
        Case.the().pvparam.params["partall"] = self.partall.text()
        Case.the().pvparam.params["partbound"] = self.partbound.text()
        Case.the().pvparam.params["partfluid"] = self.partfluid.text()
        Case.the().pvparam.params["partfixed"] = self.partfixed.text()
        Case.the().pvparam.params["partmoving"] = self.partmoving.text()
        Case.the().pvparam.params["partfloating"] = self.partfloating.text()
        Case.the().pvparam.params["forces"] = self.forces.text()
        
        file_tools.save_case(Case.the().path,Case.the())
        
        self.close()
        
def open_paraview_client():
    subprocess.Popen([Case.the().executable_paths.paraview, "--state=" + os.path.abspath(FreeCAD.getUserAppDataDir() 
        + 'Mod/DesignSPHysics/mod/paraview/pv_client.py')], stdout=subprocess.PIPE)
   
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    
    pv_param = Case.the().pvparam.params
    pv_param["name"] = Case.the().name
    pv_param["path"] = Case.the().path
    pv_param["outdir"] = Case.the().get_out_folder_path()
    
    clientMessage, clientAddress = serverSocket.recvfrom(2048)
    if clientMessage.decode() == "Client Ready":
        serverSocket.sendto(pickle.dumps(pv_param), clientAddress)
    clientMessage, clientAddress = serverSocket.recvfrom(2048)    
    serverSocket.close()
    if clientMessage.decode() != '':
        info_dialog('Not found:'+'\n'+(clientMessage.decode()).replace('-','\n')+'\n'+'\n'+'Run postprocessing tools or check settings.')
