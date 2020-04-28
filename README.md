# cea-grasshopper

A Rhino/Grasshopper interface to the [City Energy Analyst (CEA)](https://github.com/architecture-building-systems/CityEnergyAnalyst) using [honey-badger](https://github.com/architecture-building-systems/honey-badger).

## Introduction

The CEA uses a file (`scripts.yml`) to define the list of known scripts as well as their parameters. These scripts can be used with the `cea SCRIPT [PARAMETERS]` command to run the scripts that you would otherwise run via the GUI interface. In fact, that's how the GUI interface runs the scripts in the background!

`honey-badger` is a tool that takes a "badger-file" (a `.json`)as an input and produces a `.ghpy` file that can be placed in the Grasshopper "Libraries" folder.

The task of this repository, therefore, is:

- write a python script (using the CEA python environment) to create/update a badger-file 
  
  - `cea-compile-grasshopper.py`
  
  - `cea-grasshopper.json`

- define how `cea.config.Configuration.Parameter` subclasses are to be mapped to Grasshopper parameters (suggestion: just use strings)

- write a python script (using the GhPython IronPython environment) to shell out to CEA Python (using `subprocess.Popen` or similar) 
  
  - `cea_runner.py` for now

- Ideally, print progress to `RhinoApp.WriteLine`

- wrap all this stuff up and compile to `cea-grasshopper.ghpy` that can be deployed to the Grasshopper Libraries folder.

- stretch goal: publish this to [Food4Rhino](https://www.food4rhino.com/)



Since Grasshopper uses GUIDs to denote components, the `cea-compile-grasshopper.py` will make sure to re-use GUIDs from previous runs. So the output of this script (`cea-grasshopper.json`, the badgerfile) needs to be _updated_ if it already exists.
