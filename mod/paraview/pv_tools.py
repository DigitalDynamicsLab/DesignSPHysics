#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Paraview tools"""

from socket import *

import os 

import subprocess

import FreeCAD

from mod.dialog_tools import info_dialog

from mod.dataobjects.case import Case

def open_paraview_client():
    subprocess.Popen([Case.the().executable_paths.paraview, "--state=" + os.path.abspath(FreeCAD.getUserAppDataDir() 
        + 'Mod/DesignSPHysics/mod/paraview/pv_client.py')], stdout=subprocess.PIPE)
    
    # subprocess.Popen([r'C:\Program Files\ParaView 5.8.0-Windows-Python3.7-msvc2015-64bit\bin\paraview.exe',
                      # "--script=C:/Users/Penzo/AppData/Roaming/FreeCAD/Mod/DesignSPHysics/mod/paraview/pv_server.py"], stdout=subprocess.PIPE)
    
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    
    clientMessage, clientAddress = serverSocket.recvfrom(2048)
    if clientMessage.decode() == "Client Ready":
        # serverSocket.sendto(('C:/Users/penzo/Documents/DSPHProject/RheologyEstimation/rhe_est/rhe_est_out').encode(), clientAddress)
        serverSocket.sendto((Case.the().get_out_folder_path()).encode(), clientAddress)
        # for command in pvparam.commandDict:
        #     serverSocket.sendto((command+'-'+pvparam.commandDict[command]).encode(), clientAddress)
        # serverSocket.sendto(("End of command list-End").encode(), clientAddress)
    clientMessage, clientAddress = serverSocket.recvfrom(2048)    
    serverSocket.close()
    if clientMessage.decode() != '':
        info_dialog('Not found:'+'\n'+(clientMessage.decode()).replace('-','\n')+'\n'+'\n'+'Run postprocessing tools or check settings.')
      
#open_paraview_client()
    