"""
cea-compile-grasshopper.py: Create a honey-badger BADGERFILE for running CEA from Rhino/Grasshopper.

You'll need to have a working CEA installation - including the CEA Console. It is assumed that this script 
is run from the CEA Console using the version of Python shipped with the CEA.
"""
from __future__ import print_function

import os
import uuid
import json
import cea.config
import cea.scripts

BADGERFILE = os.path.join(os.path.dirname(__file__), "cea-grasshopper.json")
CATEGORY = "City Energy Analyst"  # this is the Panel to show in Grasshopper


def main():
    config = cea.config.Configuration(config_file=cea.config.DEFAULT_CONFIG)

    with open(BADGERFILE, "r") as badger_fp:
        badgerfile = json.load(badger_fp)

    # collect previous guids, if possible:
    guids = {c["name"]: c["id"] for c in badgerfile["components"]}
    print(guids)
    print()

    badgerfile["components"] = []
    for script in cea.scripts.for_interface("cli"):        
        component = {
            "id": guids[script.label] if script.label in guids else str(uuid.uuid4()),
            "class-name": "".join(s.capitalize() for s in script.name.split("-")),
            "abbreviation": "".join(s[0] for s in script.name.split("-")),
            "name": script.label,
            "description": script.description,
            "category": CATEGORY,
            "subcategory": script.category,
            # "icon": "icons/{name}.png".format(name=script.name),
            "main-module": "cea_runner",
            "main-function": script.name.replace("-", "_"),
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
        print(script.name)
        for _, parameter in config.matching_parameters(script.parameters):            
            print("\t{pname}={pvalue}".format(pname=parameter.name, pvalue=parameter.get_raw()))
            input = {
                "type": "string",
                "name": parameter.name,
                "description": parameter.help,
                "nick-name": "".join(s[0] for s in parameter.name.split("-")),
                "default": parameter.default,
                "access": "item"
            }
            component["inputs"].append(input)
        badgerfile["components"].append(component)
        

    with open(BADGERFILE, "w") as badger_fp:
        json.dump(badgerfile, badger_fp, indent=4)


if __name__ == "__main__":
    main()