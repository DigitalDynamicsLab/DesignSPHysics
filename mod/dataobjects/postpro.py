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
        self.mixingindex_spec_dir = '0'
        self.mixingindex_spec_div = '0'
        self.mixingindex_iso_surf = '0'
        self.mixingindex_part_fluid = '0'
        
        self.computeforce_mk = '11'
        
        self.mixingforces_mesh_sudiv ='2'
        
        self.mixingforces_x_point = '0'
        self.mixingforces_y_point = '0'
        self.mixingforces_z_point = '0'
        self.mixingforces_tau = '1'
        self.mixingforces_mesh_ref = '0'
        self.mixingforces_bound_vtk = '0'
        self.mixingforces_torque = '0'
        
        self.partfluid_checked = True
        self.partfixed_checked = False
        self.partmoving_checked = False
        self.boundaryvtk_checked = True
        self.isosurface_checked = True
        self.mixingindex_checked = True
        self.mixingforces_checked = True