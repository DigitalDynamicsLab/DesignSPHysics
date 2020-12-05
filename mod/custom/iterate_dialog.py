#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Non Newtonian Parameters Dialog """

import FreeCAD

import pickle
import itertools
import os
from os import path
from traceback import print_exc

from PySide import QtCore, QtGui

from mod.translation_tools import __
from mod.stdout_tools import log
from mod.stdout_tools import debug
from mod.dialog_tools import error_dialog, warning_dialog
from mod.executable_tools import refocus_cwd, ensure_process_is_executable_or_fail
from mod.file_tools import save_case
from mod.freecad_tools import get_fc_main_window, save_current_freecad_document, document_count

from mod.constants import VERSION

from mod.dataobjects.case import Case

from mod.widgets.gencase_completed_dialog import GencaseCompletedDialog
from mod.widgets.run_dialog import RunDialog

from mod.custom.nn_parameters_wizard import NNParametersWizard

class IterateDialog(QtGui.QDialog):
    
    need_refresh = QtCore.Signal()
    update_dp = QtCore.Signal()
    case_created = QtCore.Signal()
    gencase_completed = QtCore.Signal(bool)
    simulation_completed = QtCore.Signal(bool)
    force_pressed = QtCore.Signal()
    simulation_cancelled = QtCore.Signal()
    simulation_started = QtCore.Signal()
    start_iter = QtCore.Signal()
    iter_completed = QtCore.Signal()
    
    def __init__(self, parent = None, device_selector = None):
        super().__init__(parent = parent)
        
        self.device_selector = device_selector
        
        self.constants = ['rhopg','hswl','gamma','speedsystem','coefsound','speedsound',
            'coefh','cflnumber','h','b','massbound','massfluid']
        self.parameters = ['dp','verletsteps','visco','viscoboundfactor','densitydt_value','shiftcoef','shifttfs','ftpause','coefdtmin','dtini','dtmin',
            'dtallparticles','timemax','timeout','rhopoutmin','rhopoutmax']
        self.nn_constants = ['rhop','viscop','tau_yield','tau_max','Bi_multi','HBP_m','HBP_n']

        self.param_names = {'dp':'DP',
                            'rhopg':'RG',
                            'hswl':'HL',
                            'gamma':'G',
                            'speedsystem':'MS',
                            'coefsound':'CS',
                            'speedsound':'SS',
                            'coefh':'CH',
                            'cflnumber':'CFL',
                            'h':'H',
                            'b':'B',
                            'massbound':'MB',
                            'massfluid':'MF',
                            'verletsteps':'VS',
                            'visco':'VG',
                            'viscoboundfactor':'VB',
                            'densitydt_value':'DDT',
                            'shiftcoef':'SH',
                            'shifttfs':'SHF',
                            'ftpause':'ftpause',
                            'coefdtmin':'CT',
                            'dtini':'TI',
                            'dtmin':'Tm',
                            'dtallparticles':'TA',
                            'timemax':'TM',
                            'timeout':'TO',
                            'rhopoutmin':'RGm',
                            'rhopoutmax':'RGM',
                            'rhop':'R',
                            'viscop':'V',
                            'tau_yield':'Y',
                            'tau_max':'YM',
                            'Bi_multi':'Bm',
                            'HBP_m':'Cm',
                            'HBP_n':'Cn'}        
        
        self.simulation_is_cancelled = False
        self.simulation_cancelled.connect(self.on_cancel_simulate)
        self.iter_completed.connect(self.on_ex_iterate)
                
        self.iter_num = 0
        self.save_name_list = []
        
        self.setModal(False)
        self.title = 'Iterate options'
        self.left = 0
        self.top = 0
        self.width = 400
        self.height = 400
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
                
        self.search_entry = QtGui.QLineEdit()
        self.search_entry.setPlaceholderText("Search param...")
        self.search_entry.textChanged.connect(self.on_search_entry)
        
        self.search_entry_layout = QtGui.QHBoxLayout()
        self.search_entry_layout.addWidget(self.search_entry) 
        
        self.search_results = QtGui.QListWidget()
        self.search_results.itemClicked.connect(self.on_search_result)
        
        self.search_results_layout = QtGui.QHBoxLayout()
        self.search_results_layout.addWidget(self.search_results)   
        
        self.main_layout = QtGui.QVBoxLayout()        
        self.main_layout.addLayout(self.search_entry_layout)
        self.main_layout.addLayout(self.search_results_layout)
        
        self.setLayout(self.main_layout)
                     
        self.iteration_params_labels = []
        self.iteration_params_lines = []
        self.iteration_params_layout = QtGui.QVBoxLayout()
        
        self.iterate_button = QtGui.QPushButton("Iterate")
        self.iterate_button.clicked.connect(self.on_prepare_iterate)
        
        self.buttons_layout = QtGui.QHBoxLayout()
        self.buttons_layout.addWidget(self.iterate_button)
        
        self.need_refresh.connect(parent.need_refresh.emit)
        
        self.on_search_entry()
        self.center()  
        self.exec_()
    
    def on_cancel_simulate(self):
        self.simulation_is_cancelled = True
        
    def on_prepare_iterate(self):
        self.close()     
        param_values = []
        for i in range(0,len(self.iteration_params_labels)):
            if len(self.iteration_params_lines[i].text().split(',')) >= 1:
                param_values.append(self.iteration_params_lines[i].text().split(','))
            else:
                self.iteration_params_labels.remove(self.iteration_params_labels[i])
                                
        self.combinations_list = []
        combinations = itertools.product(*param_values)
        self.total_iters = 0
        for params_combination in combinations:
            self.total_iters += 1
            self.combinations_list.append(params_combination)
        
        self.case_original_path = Case.the().path   
        self.on_ex_iterate()
              
    def on_ex_iterate(self):
        #self.iteration_params_labels.sort()
        if self.iter_num != self.total_iters and self.simulation_is_cancelled != True:
            params_combination = self.combinations_list[self.iter_num]
            save_name = ''
            nn_target_params = []          
            for i in range(0,len(self.iteration_params_labels)):          
                if self.iteration_params_labels[i] in self.constants:
                    if self.iteration_params_labels[i] == 'rhopg':
                        exec('Case.the().constants.rhop0 = float('+params_combination[i]+')')
                    else:
                        exec('Case.the().constants.'+self.iteration_params_labels[i]+'= float('+params_combination[i]+')')
                
                elif self.iteration_params_labels[i] in self.parameters:
                    if self.iteration_params_labels[i] == 'dp':
                        Case.the().dp = params_combination[i]
                    else:
                        exec('Case.the().execution_parameters.'+self.iteration_params_labels[i]+'= float('+params_combination[i]+')')
                
                elif self.iteration_params_labels[i] in self.nn_constants:
                    if self.iteration_params_labels[i] == 'viscop':
                        nn_target_params.append(['visco',params_combination[i]])
                        exec('Case.the().execution_parameters.visco = float('+params_combination[i]+')')
                    elif self.iteration_params_labels[i] == 'rhop':
                        nn_target_params.append(['rhop',params_combination[i]])
                        exec('Case.the().constants.rhop0 = float('+params_combination[i]+')')
                    elif self.iteration_params_labels[i] == 'tau_yield':
                        nn_target_params.append(['tau_yield',params_combination[i]])
                        nn_target_params.append(['tau_max',params_combination[i]])
                    else:
                        nn_target_params.append([self.iteration_params_labels[i],params_combination[i]]) 
                
                param_name = self.param_names[self.iteration_params_labels[i]]
                save_name = save_name + param_name + str("{:.1e}".format(float(params_combination[i])/10))
                save_name = save_name.replace('.','')
                save_name = save_name.replace('e+','E')
                save_name = save_name.replace('e-','e')
            self.on_save_case(save_name = self.case_original_path + save_name) 
            self.on_execute_gencase(nn_target_params)
            self.device_selector.setCurrentIndex(1) 
            self.on_ex_simulate()
            self.iter_num += 1
    
    def on_search_result(self):   
        i = len(self.iteration_params_labels)    
        if not self.search_results.currentItem().text() in self.iteration_params_labels:
            
            self.iteration_params_labels.append(self.search_results.currentItem().text())
            self.iteration_params_lines.append(QtGui.QLineEdit())
            
            self.iteration_params_row_layout = QtGui.QHBoxLayout()
            self.iteration_params_row_layout.addWidget(QtGui.QLabel(self.search_results.currentItem().text()))  
            self.iteration_params_row_layout.addWidget(self.iteration_params_lines[i])  
            
            self.iteration_params_layout.addLayout(self.iteration_params_row_layout)
            self.main_layout.addLayout(self.iteration_params_layout)
        
        if i == 0:
            self.main_layout.addLayout(self.buttons_layout)
        
    def on_search_entry(self):
        self.search_results.clear()
        for var in self.constants + self.parameters + self.nn_constants:
            if var.find(self.search_entry.text()) == 0:
                self.search_results.addItem(var)
        
    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
               
    def on_load_case(self,load_path):
        """Defines loading case mechanism. Load points to a dsphdata custom file, that stores all the relevant info.
           If FCStd file is not found the project is considered corrupt."""
        def load_case(load_path: str) -> "Case":
            """ Loads a case from the given folder and returns its Case data. """
            refocus_cwd()
            project_folder_path = path.dirname(load_path)
            freecad_document_file_path = path.abspath("{}/DSPH_Case.FCStd".format(project_folder_path))
        
            if not path.isfile(freecad_document_file_path):
                error_dialog(__("DSPH_Case.FCStd file could not be found. Please check if the project was moved or the file was renamed."))
                return None
        
            if document_count():
                return None
        
            FreeCAD.open(project_folder_path + "/DSPH_Case.FCStd")
        
            with open(load_path, "rb") as load_picklefile:
                try:
                    loaded_data = pickle.load(load_picklefile)
                    if not loaded_data.version:
                        warning_dialog(__("The case data you're trying to load is older than version 0.6 and cannot be loaded."))
                        return None
                    if loaded_data.version < VERSION:
                        warning_dialog(__("The case data you are loading is from a previous version ({}) of this software. They may be missing features or errors.").format(loaded_data.version))
                    elif loaded_data.version > VERSION:
                        warning_dialog(__("You're loading a case data from a future version ({}) of this software. You should upgrade DesignSPHysics as they may be errors using this file.").format(loaded_data.version))
        
                    return loaded_data
                except AttributeError:
                    error_dialog(__("There was an error opening the case. Case Data file seems to be corrupted."))
                    return None
        
        Case.the().info.update_last_used_directory(load_path)

        if load_path == "":
            return

        disk_data: Case = load_case(load_path)
        if not disk_data:
            return

        try:
            Case.update_from_disk(disk_data)
            self.update_dp.emit()
        except (EOFError, ValueError):
            error_dialog(__("There was an error importing the case  You probably need to set them again.\n\n"
                            "This could be caused due to file corruption, caused by operating system based line endings or ends-of-file, or other related aspects."))

        # User may have changed the name of the folder/project
        Case.the().path = path.dirname(load_path)
        Case.the().name = Case.the().path.split("/")[-1]

        # Adapt widget state to case info
        self.case_created.emit()
        self.gencase_completed.emit(Case.the().info.is_gencase_done)
        self.simulation_completed.emit(Case.the().info.is_simulation_done)
        self.need_refresh.emit()

        Case.the().executable_paths.check_and_filter()
        Case.the().info.update_last_used_directory(load_path)
        
    def on_save_case(self, save_as=None , save_name=None):
        """ Defines what happens when save case button is clicked.
        Saves a freecad scene definition, and a dump of dsph data for the case."""
        if save_name is None:
            if Case.the().was_not_saved() or save_as:
                save_name, _ = QtGui.QFileDialog.getSaveFileName(self, __("Save Case"), Case.the().info.last_used_directory)
                Case.the().info.update_last_used_directory(save_name)
            else:
                save_name = Case.the().path

            if not save_name:
                return

        Case.the().info.needs_to_run_gencase = True
        save_case(save_name, Case.the())
        save_current_freecad_document(Case.the().path)
        if Case.the().has_materials() and Case.the().execution_parameters.rigidalgorithm not in (2, 3):
            warning_dialog(
                __("Properties and Material information wasn't written. See details for more info."),
                __("The case being saved has some properties/materials defined in one of its MKs.\n"
                   "However, the solid-solid interaction on the execution parameters must be set to DEM or CHRONO for this feature to work.")
            )
        self.need_refresh.emit()

    def on_execute_gencase(self,nn_target_params=None):
        """ Saves data into disk and uses GenCase to generate the case files."""
        self.on_save_case()
        if not Case.the().executable_paths.gencase:
            warning_dialog(__("GenCase executable is not set."))
            return

        gencase_full_path = path.abspath(Case.the().executable_paths.gencase)
        arguments = ["{path}/{name}_Def".format(path=Case.the().path, name=Case.the().name),
                     "{path}/{name}_out/{name}".format(path=Case.the().path, name=Case.the().name),
                     "-save:+all"]
        cmd_string = "{} {}".format(gencase_full_path, " ".join(arguments))

        refocus_cwd()
        process = QtCore.QProcess(get_fc_main_window())
        process.setWorkingDirectory(Case.the().path)
        ensure_process_is_executable_or_fail(gencase_full_path)
        process.start(gencase_full_path, arguments)
        debug("Executing -> {}".format(cmd_string))
        process.waitForFinished()

        try:
            output = str(process.readAllStandardOutput().data(), encoding='utf-8')
        except UnicodeDecodeError:
            output = str(process.readAllStandardOutput().data(), encoding='latin1')

        if process.exitCode():
            Case.the().info.is_gencase_done = False
            error_dialog(__("Error executing GenCase. Did you add objects to the case?. Another reason could be memory issues. View details for more info."), output)
        else:
            try:
                total_particles_text = output[output.index("Total particles: "):output.index(" (bound=")]
                total_particles = int(total_particles_text[total_particles_text.index(": ") + 2:])
                Case.the().info.particle_number = total_particles
                if NNParametersWizard().nn_options_xml_exists:
                    NNParametersWizard().update_nn_parameters(nn_target_params)
                #GencaseCompletedDialog(particle_count=total_particles, detail_text=output, cmd_string=cmd_string, parent=get_fc_main_window()).show()
                Case.the().info.is_gencase_done = True
                self.on_save_case()
                Case.the().info.needs_to_run_gencase = False
            except ValueError:
                print_exc()
                Case.the().info.is_gencase_done = False
                Case.the().info.needs_to_run_gencase = True

        # Refresh widget enable/disable status as GenCase finishes
        self.gencase_completed.emit(Case.the().info.is_gencase_done)
        
    def on_ex_simulate(self):
        """ Defines what happens on simulation button press.
            It shows the run window and starts a background process with dualsphysics running. Updates the window with useful info."""

        refocus_cwd()

        #if Case.the().info.needs_to_run_gencase:
            # Warning window about save_case
            #warning_dialog("You should run GenCase again. Otherwise, the obtained results may not be as expected")

        static_params_exe = [Case.the().get_out_xml_file_path(),
                             Case.the().get_out_folder_path(),
                             "-{device}".format(device=self.device_selector.currentText().lower()),
                             "-svres"]

        additional_parameters = list()
        if Case.the().info.run_additional_parameters:
            additional_parameters = Case.the().info.run_additional_parameters.split(" ")

        final_params_ex = static_params_exe + additional_parameters
        cmd_string = "{} {}".format(Case.the().executable_paths.dsphysics, " ".join(final_params_ex))
        
        iter_name = Case.the().name+' ('+str(self.iter_num + 1)+' of '+str(self.total_iters)+' iterations)'
        run_dialog = RunDialog(case_name=iter_name, processor=self.device_selector.currentText(), number_of_particles=Case.the().info.particle_number, cmd_string=cmd_string, parent=get_fc_main_window())
        run_dialog.set_value(0)
        run_dialog.run_update(0, 0, None)
        Case.the().info.is_simulation_done = False

        run_fs_watcher = QtCore.QFileSystemWatcher()

        self.simulation_started.emit()

        # Cancel button handler
        def on_cancel():
            log(__("Stopping simulation"))
            if process:
                process.kill()
            run_dialog.hide_all()
            Case.the().info.is_simulation_done = True
            self.simulation_cancelled.emit()

        run_dialog.cancelled.connect(on_cancel)

        # Launch simulation and watch filesystem to monitor simulation
        filelist = [f for f in os.listdir(Case.the().path + "/" + Case.the().name + "_out/") if f.startswith("Part")]
        for f in filelist:
            if not os.path.isdir(Case.the().path + "/" + Case.the().name + "_out/" + f):
                os.remove(Case.the().path + "/" + Case.the().name + "_out/" + f)

        def on_dsph_sim_finished(exit_code):
            """ Simulation finish handler. Defines what happens when the process finishes."""

            # Reads output and completes the progress bar
            try:
                output = str(process.readAllStandardOutput().data(), encoding='utf-8')
            except UnicodeDecodeError:
                output = str(process.readAllStandardOutput().data(), encoding='latin1')

            run_dialog.set_detail_text(str(output))
            run_dialog.run_complete()

            run_fs_watcher.removePath(Case.the().path + "/" + Case.the().name + "_out/")

            if exit_code == 0:
                # Simulation went correctly
                Case.the().info.is_simulation_done = True
                Case.the().info.needs_to_run_gencase = False
                self.simulation_completed.emit(True)
                self.iter_completed.emit()
            else:
                # In case of an error
                Case.the().info.needs_to_run_gencase = True
                if "exception" in str(output).lower():
                    log("There was an error on the execution. Opening an error dialog for that.")
                    run_dialog.hide()
                    self.simulation_completed.emit(False)
                    error_dialog(__("An error occurred during execution. Make sure that parameters exist and are properly defined. "
                                    "You can also check your execution device (update the driver of your GPU). Read the details for more information."), str(output))
            save_case(Case.the().path, Case.the())

        # Launches a QProcess in background
        process = QtCore.QProcess(get_fc_main_window())
        process.finished.connect(on_dsph_sim_finished)

        ensure_process_is_executable_or_fail(Case.the().executable_paths.dsphysics)
        process.start(Case.the().executable_paths.dsphysics, final_params_ex)

        def on_fs_change():
            """ Executed each time the filesystem changes. This updates the percentage of the simulation and its details."""
            run_file_data = ""
            with open(Case.the().path + "/" + Case.the().name + "_out/Run.out", "r", encoding="utf-8") as run_file:
                run_file_data = run_file.readlines()

            # Fill details window
            run_dialog.set_detail_text("".join(run_file_data))

            # Set percentage scale based on timemax
            for l in run_file_data:
                if Case.the().execution_parameters.timemax == -1:
                    if "TimeMax=" in l:
                        Case.the().execution_parameters.timemax = float(l.split("=")[1])

            current_value: float = 0.0
            totalpartsout: int = 0
            last_estimated_time = None

            # Update execution metrics
            last_part_lines = list(filter(lambda x: "Part_" in x and "stored" not in x and "      " in x, run_file_data))
            if last_part_lines:
                current_value = (float(last_part_lines[-1].split(None)[1]) * float(100)) / float(Case.the().execution_parameters.timemax)
            else:
                current_value = None

            # Update particles out
            last_particles_out_lines = list(filter(lambda x: "(total: " in x and "Particles out:" in x, run_file_data))
            if last_particles_out_lines:
                totalpartsout = int(last_particles_out_lines[-1].split("(total: ")[1].split(")")[0])

            try:
                last_estimated_time = str(" ".join(last_part_lines[-1].split(None)[-2:]))
            except IndexError:
                last_estimated_time = None

            # Update run dialog
            run_dialog.run_update(current_value, totalpartsout, last_estimated_time)

        # Set filesystem watcher to the out directory.
        run_fs_watcher.addPath(Case.the().path + "/" + Case.the().name + "_out/")
        run_fs_watcher.directoryChanged.connect(on_fs_change)

        # Handle error on simulation start
        if process.state() == QtCore.QProcess.NotRunning:
            # Probably error happened.
            run_fs_watcher.removePath(Case.the().path + "/" + Case.the().name + "_out/")
            process = None
            error_dialog("Error on simulation start. Check that the DualSPHysics executable is correctly set.")
        else:
            run_dialog.show()
        