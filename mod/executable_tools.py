#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

""" Executable related tools. """

from os import path, environ, chdir, stat, chmod, access, X_OK
import stat as unix_stat
from sys import platform
import json

from PySide import QtCore

import FreeCADGui

from mod.translation_tools import __
from mod.constants import APP_NAME


def executable_contains_string(executable: str, string: str) -> bool:
    """ Returns whether the standard output of the executable contains the passed string.
        The string passed as a parameters is not case sensitive. """
    refocus_cwd()
    if path.isfile(executable):
        process = QtCore.QProcess(FreeCADGui.getMainWindow())

        if platform in ("linux", "linux2"):
            environ["LD_LIBRARY_PATH"] = path.dirname(executable)

        ensure_process_is_executable_or_fail(executable)
        process.start("\"{}\" -ver".format(executable))
        process.waitForFinished()
        output = str(process.readAllStandardOutput().data(), encoding='utf-8')

        return string.lower() in output.lower()

    return False


def get_executable_info_flag(executable: str) -> dict:
    """ Returns a dictionary with the JSON generated by the -info flag on the
        DualSPHysics package executables. """
    refocus_cwd()
    if path.isfile(executable):
        process = QtCore.QProcess(FreeCADGui.getMainWindow())

        if platform in ("linux", "linux2"):
            environ["LD_LIBRARY_PATH"] = path.dirname(executable)

        executable_cli = "\"{}\" -info".format(executable)
        ensure_process_is_executable_or_fail(executable)
        process.start(executable_cli)
        process.waitForFinished()
        output = str(process.readAllStandardOutput().data(), encoding='utf-8')

        return json.loads(output)

    return None


def refocus_cwd():
    """ Ensures the current working directory is the DesignSPHysics folder """
    chdir("{}/..".format(path.dirname(path.abspath(__file__))))


def are_executables_bundled():
    """ Returns if the DualSPHysics executable directory exists"""
    dsph_execs_path = "{}/../dualsphysics/bin/".format(path.dirname(path.realpath(__file__)))
    return path.isdir(dsph_execs_path)


def ensure_process_is_executable_or_fail(cli_path: str) -> None:
    """ Ensures and asserts a process is executable or fails and raises an exception. """
    if platform in ("linux", "linux2"):
        st = stat(cli_path)
        chmod(cli_path, st.st_mode | unix_stat.S_IEXEC)
    if not access(cli_path, X_OK):
        raise RuntimeError(__("The executable {} doesn't have executable permissions and {} cant provide it for you. Please give execution permissions to that file.").format(cli_path, APP_NAME))
