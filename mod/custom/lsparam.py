#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics case Liquid-Sediment parameters dataobject """

class LsParam():
    """ DualSPHysics case Liquid-Sediment parameters dataobject. """
    
    def __init__(self):
        self.eps = '0.0'
        self.deltasph = '0.1'
        
        self.tabs_list = []

class LsDict():
            
    def __init__(self):    
        self.phase_dict = {'mk':'0',
                           'density':'1000',
                           'csound':'20',
                           'gamma':'7',
                           'viscosity':'0.01',
                           'HBP_n':'1',
                           'HBP_m':'100',
                           'cohesion':'1.0',
                           'reposeangle':'30',
                           'constantyield':'0',
                           'phase_type':'1'}
      