#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics case Post Processing parameters dataobject """

class PostPro():
    """ DualSPHysics case Post Processing parameters dataobject. """

    def __init__(self):
        self.mixingquality_timestep = '1'
        self.mixingquality_first_step = '0'
        self.mixingquality_type_div = '0'
        self.mixingquality_1dim_div = '10'
        self.mixingquality_2dim_div = '1'
        self.mixingquality_3dim_div = '1'
        self.mixingquality_axial_dir = '0'
        self.mixingquality_spec_dir = '0'
        self.mixingquality_spec_div = '0'        
        self.mixingquality_calc_type = '0'
        self.mixingquality_up_type = '0'
        self.mixingquality_iso_type = '0'
        self.mixingquality_coef_dp = '2'
        self.mixingquality_sub_dir = ''
        
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
        self.mixingquality_checked = True
        self.mixingforces_checked = True