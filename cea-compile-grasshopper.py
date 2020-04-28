"""
cea-compile-grasshopper.py: Create a honey-badger BADGERFILE for running CEA from Rhino/Grasshopper.

You'll need to have a working CEA installation - including the CEA Console. It is assumed that this script 
is run from the CEA Console using the version of Python shipped with the CEA.
"""
from __future__ import print_function

import os
import uuid
import json
import shutil
import cea.config
import cea.scripts

BADGERFILE = os.path.join(os.path.dirname(__file__), "cea-grasshopper.json")
SCRIPTS_FILE = os.path.join(os.path.dirname(__file__), "cea_scripts.py")
SCRIPT_DEF_TEMPLATE_FILE = os.path.join(os.path.dirname(__file__), "script_def.py")
CATEGORY = "City Energy Analyst"  # this is the Panel to show in Grasshopper


def main():
    config = cea.config.Configuration(config_file=cea.config.DEFAULT_CONFIG)
    script_defs = []  # a list of script defs in SCRIPTS_FILE
    
    with open(SCRIPT_DEF_TEMPLATE_FILE, "r") as script_def_fp:
        script_def_template = script_def_fp.read()

    with open(BADGERFILE, "r") as badger_fp:
        badgerfile = json.load(badger_fp)

    # collect previous guids, if possible:
    guids = {c["name"]: c["id"] for c in badgerfile["components"]}
    
    badgerfile["components"] = []
    for script in cea.scripts.for_interface("cli"):
        script_py_name = script.name.replace("-", "_") 
        component = {
            "id": guids[script.label] if script.label in guids else str(uuid.uuid4()),
            "class-name": "".join(s.capitalize() for s in script.name.split("-")),
            "abbreviation": "".join(s[0] for s in script.name.split("-")),
            "name": script.label,
            "description": script.description,
            "category": CATEGORY,
            "subcategory": script.category,
            "icon": "icons/{name}.png".format(name=script.name),           
            "main-module": "cea_scripts",
            "main-function": script_py_name,
            "use-kwargs": True,
            "inputs": [
                {
                    "type": "string",
                    "name": "config",
                    "description": "Configuration file (path or contents)",
                    "nick-name": "ci"
                }
            ],
            "outputs": [
                {
                    "type": "string",
                    "name": "config",
                    "description": "Configuration file contents",
                    "nick-name": "co"
                }
            ],
        }
        script_defs.append(script_def_template.replace("SCRIPT_PY_NAME", script_py_name).replace("SCRIPT_NAME", script.name))
        print(script.name)
        for _, parameter in config.matching_parameters(script.parameters):            
            print("\t{pname}={pvalue}".format(pname=parameter.name, pvalue=parameter.get_raw()))
            input = {
                "type": "string",
                "name": parameter.fqname,
                "description": parameter.help,
                "nick-name": parameter.name,
                "default": parameter.default,
                "access": "item"
            }
            component["inputs"].append(input)
        badgerfile["components"].append(component)

        # copy the icon if it doesn't exist yet
        icon_path = os.path.join(os.path.dirname(__file__), component["icon"])
        default_icon_path = os.path.join(os.path.dirname(__file__), "default_icon.png")
        if not os.path.exists(icon_path):
            shutil.copyfile(default_icon_path, icon_path)
        

    with open(BADGERFILE, "w") as badger_fp:
        json.dump(badgerfile, badger_fp, indent=4)

    with open(SCRIPTS_FILE, "w") as scripts_fp:
        scripts_fp.write("\n".join(script_defs))


if __name__ == "__main__":
    main()