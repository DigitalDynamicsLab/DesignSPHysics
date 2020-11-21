#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Dock Post Processing Widget """

import subprocess

from PySide import QtGui

from mod.dataobjects.case import Case

from mod.translation_tools import __
from mod.freecad_tools import get_fc_main_window

from mod.widgets.postprocessing.partvtk_dialog import PartVTKDialog
from mod.widgets.postprocessing.computeforces_dialog import ComputeForcesDialog
from mod.widgets.postprocessing.floatinginfo_dialog import FloatingInfoDialog
from mod.widgets.postprocessing.measuretool_dialog import MeasureToolDialog
from mod.widgets.postprocessing.isosurface_dialog import IsoSurfaceDialog
from mod.widgets.postprocessing.flowtool_dialog import FlowToolDialog

from mod.custom.advanced_post_processing_dialog import AdvancedPostProcessingDialog
from mod.custom.paraview.pv_tools import PvSettingsDialog
from mod.custom.paraview.pv_tools import open_paraview_client

class DockPostProcessingWidget(QtGui.QWidget):
    """DesignSPHysics Dock Post Processing Widget """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Post processing section scaffolding
        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.title_label = QtGui.QLabel("<b>{}</b>".format(__("Post-processing")))
        self.title_label.setWordWrap(True)

        self.first_row_layout = QtGui.QHBoxLayout()
        self.second_row_layout = QtGui.QHBoxLayout()

        self.partvtk_button = QtGui.QPushButton(__("PartVTK"))
        self.computeforces_button = QtGui.QPushButton(__("ComputeForces"))
        self.isosurface_button = QtGui.QPushButton(__("IsoSurface"))
        self.floatinginfo_button = QtGui.QPushButton(__("FloatingInfo"))
        self.measuretool_button = QtGui.QPushButton(__("MeasureTool"))
        self.flowtool_button = QtGui.QPushButton(__("FlowTool"))
        self.advanced_button = QtGui.QPushButton(__("Advanced"))
        
        self.paraview_button = QtGui.QPushButton(__("Paraview"))
        self.paraview_menu = QtGui.QMenu()
        self.paraview_menu.addAction(__("Open Paraview"))
        self.paraview_menu.addAction(__("Options"))
        self.paraview_menu.triggered.connect(self.on_paraview_menu)
        self.paraview_button.setMenu(self.paraview_menu)

        self.partvtk_button.setToolTip(__("Opens the PartVTK tool."))
        self.computeforces_button.setToolTip(__("Opens the ComputeForces tool."))
        self.floatinginfo_button.setToolTip(__("Opens the FloatingInfo tool."))
        self.measuretool_button.setToolTip(__("Opens the MeasureTool tool."))
        self.isosurface_button.setToolTip(__("Opens the IsoSurface tool."))
        self.flowtool_button.setToolTip(__("Opens the FlowTool tool."))
        self.advanced_button.setToolTip(__("Opens the AdvancedPostProcessing tool."))
        self.paraview_button.setToolTip(__("Paraview results menu."))

        self.partvtk_button.clicked.connect(lambda: PartVTKDialog(self, parent=get_fc_main_window()))
        self.computeforces_button.clicked.connect(lambda: ComputeForcesDialog(self, parent=get_fc_main_window()))
        self.floatinginfo_button.clicked.connect(lambda: FloatingInfoDialog(self, parent=get_fc_main_window()))
        self.measuretool_button.clicked.connect(lambda: MeasureToolDialog(self, parent=get_fc_main_window()))
        self.isosurface_button.clicked.connect(lambda: IsoSurfaceDialog(self, parent=get_fc_main_window()))
        self.flowtool_button.clicked.connect(lambda: FlowToolDialog(self, parent=get_fc_main_window()))
        self.advanced_button.clicked.connect(lambda: AdvancedPostProcessingDialog(self, parent=get_fc_main_window()))

        self.main_layout.addWidget(self.title_label)
        self.first_row_layout.addWidget(self.partvtk_button)
        self.first_row_layout.addWidget(self.computeforces_button)
        self.first_row_layout.addWidget(self.isosurface_button)
        self.first_row_layout.addWidget(self.floatinginfo_button)
        self.second_row_layout.addWidget(self.measuretool_button)
        self.second_row_layout.addWidget(self.flowtool_button)
        self.second_row_layout.addWidget(self.advanced_button)
        self.second_row_layout.addWidget(self.paraview_button)

        self.main_layout.addLayout(self.first_row_layout)
        self.main_layout.addLayout(self.second_row_layout)

        self.setLayout(self.main_layout)
    
    def on_paraview_menu(self,action):
        if __("Open Paraview") in action.text():
            open_paraview_client()
        elif __("Options") in action.text():
            PvSettingsDialog(self)
            
    def adapt_to_export_start(self) -> None:
        """ Adapts the widget to post processing tool start. """
        self.setWindowTitle("<b>{} ({})</b>".format(__("Post-processing"), __("Exporting")))
        self.setEnabled(False)

    def adapt_to_export_finished(self) -> None:
        """ Adapts the widget to post processing tool finis. """
        self.setEnabled(True)
        self.setWindowTitle("<b>{}</b>".format(__("Post-processing")))
