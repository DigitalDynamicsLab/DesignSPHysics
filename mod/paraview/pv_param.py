#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Paraview parameters"""

class PvParam:

    def __init__(self):
        self.params = {"boundaryfixed":"Boundary",
                       "boundarymoving":"BoundaryMoving",
                       "isosurface":"IsoSurface",
                       "partall":"PartAll",
                       "partbound":"PartBound",
                       "partfluid":"PartFluid",
                       "partfixed":"PartFixed",
                       "partmoving":"PartMoving",
                       "partfloating":"PartFloating",
                       "forces":"Forces"}

