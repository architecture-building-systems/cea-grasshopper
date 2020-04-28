"""
cea_runner.py: This is the script that get's called from honey-badger/Grasshopper to solve
a component. It shells out to CEA to do the computation.

Each script has a "config" parameter that goes in and a "config" parameter that goes out.
The config going in is either a path to a config file OR the contents of the config file in INI
format. The config going out is the contents of the config file (updated with the parameters passed to the 
component) going out and is produced _after_ the script has run.

Script output is sent to RhinoApp.WriteLine.

The function __run_cea is used to run a cea script. It assumes the first parameter is the script name
and returns the updated config file - CEA scripts don't really have a return value, though it might
be an idea to add a list of files (possibly) produced. I'll look into that later.

We use the technique specified here: http://stackoverflow.com/questions/2447353/getattr-on-a-module
to add the scripts automatically to the module.
"""

class CeaRunner(object):
    def run(script, )
    def __getattr__(self, name):
        if not name in self.elementFactories:
            self.__createElementFactory(name)
        return self.elementFactories[name]