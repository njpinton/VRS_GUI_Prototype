import cx_Freeze
import matplotlib
import tkinter
import scipy
import os

base = None

executables = [cx_Freeze.Executable("sample_entry.py", base=base, icon="nm-logo-transparent.ico")]
additional_mods = ["sounddevice","librosa","numpy.core._methods", "numpy.lib.format","pkg_resources._vendor"]
include_files = ["sv","configuration.py","utils_deployment.py"]
scipy_path = os.path.dirname(scipy.__file__)
include_files.append(scipy_path)


cx_Freeze.setup(
    name = "NM_SV",
    options = {"build_exe": {"packages": additional_mods, 
                             "include_files":include_files}
                },
    version = "0.1",
    description = "Basic GUI for VRS",
    executables = executables
    )


