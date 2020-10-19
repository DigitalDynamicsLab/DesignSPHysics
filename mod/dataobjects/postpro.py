#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics case pospro dataobject """

class PostPro():
    """ DualSPHysics case postpro definition dataobject. """

    def __init__(self):
        self.mixingindex_timestep = '1'
        self.mixingindex_x_subdiv = '10'
        self.mixingindex_y_subdiv = '1'
        self.mixingindex_z_subdiv = '1'
        
        self.computeforce_mk = '11'
        
        self.mixingtorque_x_point = '0'
        self.mixingtorque_y_point = '0'
        self.mixingtorque_z_point = '0'
        self.mixingtorque_tau = '1'
        
        self.partfluid_checked = True
        self.partfixed_checked = False
        self.partmoving_checked = False
        self.boundaryvtk_checked = True
        self.isosurface_checked = True
        self.mixingindex_checked = True
        self.mixingtorque_checked = True