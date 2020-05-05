"""
cea_runner.py: This is the script that get's called from honey-badger/Grasshopper to solve
a component. It shells out to CEA to do the computation.

Script output is sent to RhinoApp.WriteLine.

The function "run" is used to run a cea script. It assumes the first parameter is the script name.

We use the technique specified here: http://stackoverflow.com/questions/2447353/getattr-on-a-module
to add the scripts automatically to the module.
"""
import sys
import os
import subprocess
import Rhino
import System.Windows.Forms
import System.Threading

def get_python_exe_and_env():
    """
    Try really hard to find the CEA python executable. Also, return the environment to use.
    For now: Assume CEA is installed in the default place.
    """
    cea_path = os.path.expandvars(os.path.join("${userprofile}", "Documents", "CityEnergyAnalyst"))
    python_path = os.path.join(cea_path, "Dependencies", "Python")
    python_exe = os.path.join(python_path, "python.exe")

    if not os.path.exists(python_exe):
        raise Exception("Could not fine python executable here: {python_exe}".format(python_exe=python_exe))

    # copying this stuff from dashboard.bat
    env = os.environ.copy()
    env["PATH"] = os.pathsep.join((
        python_path,
        os.path.join(python_path, "Scripts"),
        os.path.join(cea_path, "Dependencies", "Daysim"),
        env["PATH"]))
    env["PYTHONHOME"] = python_path
    env["GDAL_DATA"] = os.path.join(python_path, "Library", "share", "gdal")
    env["PROJ_LIB"] = os.path.join(python_path, "Library", "share")
    env["RAYPATH"] = os.path.join(cea_path, "Dependencies", "Daysim")
    return python_exe, env

def run(script, parameters):
    """Shell out to CEA"""
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    python_exe, env = get_python_exe_and_env()
    command = [python_exe, '-u', '-m', 'cea.interfaces.cli.cli', script]
    for parameter_name, parameter_value in parameters.items():
        if parameter_name == "config":
            # we're ignoring this for the moment
            continue
        Rhino.RhinoApp.WriteLine("Working on parameter: {parameter_name}".format(parameter_name=parameter_name))
        section_name, parameter_name = parameter_name.split(":")
        command.append('--' + parameter_name)
        command.append(str(parameter_value))

    Rhino.RhinoApp.WriteLine('Executing: ' + ' '.join(command))

    process = subprocess.Popen(command, startupinfo=startupinfo, 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    while True:
        next_line = process.stdout.readline()
        if next_line == '' and process.poll() is not None:
            break
        Rhino.RhinoApp.WriteLine(next_line.rstrip())
        System.Threading.Thread.Sleep(100)
    stdout, stderr = process.communicate()
    Rhino.RhinoApp.WriteLine(stdout)
    Rhino.RhinoApp.WriteLine(stderr)
    if process.returncode != 0:
        raise Exception('Tool did not run successfully')
