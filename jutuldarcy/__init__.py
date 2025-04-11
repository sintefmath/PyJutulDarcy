
# The following code that handles juliacall issues is copied from PySR
# Copyright 2020 Miles Cranmer, Apache 2.0 License.
# Source: https://github.com/MilesCranmer/PySR/blob/cd055a67728eeb675c76dedfe5d5e669eea3a6d1/pysr/julia_import.py
import os
import sys
import warnings
if "juliacall" in sys.modules:
    warnings.warn(
        "juliacall module already imported. "
        "Make sure that you have set the environment variable `PYTHON_JULIACALL_HANDLE_SIGNALS=yes` to avoid segfaults. "
        "Also note that PySR will not be able to configure `PYTHON_JULIACALL_THREADS` or `PYTHON_JULIACALL_OPTLEVEL` for you."
    )
else:
    # Required to avoid segfaults (https://juliapy.github.io/PythonCall.jl/dev/faq/)
    if os.environ.get("PYTHON_JULIACALL_HANDLE_SIGNALS", "yes") != "yes":
        warnings.warn(
            "PYTHON_JULIACALL_HANDLE_SIGNALS environment variable is set to something other than 'yes' or ''. "
            + "You will experience segfaults if running with multithreading."
        )

    if os.environ.get("PYTHON_JULIACALL_THREADS", "auto") != "auto":
        warnings.warn(
            "PYTHON_JULIACALL_THREADS environment variable is set to something other than 'auto', "
            "so PySR was not able to set it. You may wish to set it to `'auto'` for full use "
            "of your CPU."
        )

    # TODO: Remove these when juliapkg lets you specify this
    for k, default in (
        ("PYTHON_JULIACALL_HANDLE_SIGNALS", "yes"),
        ("PYTHON_JULIACALL_THREADS", "auto"),
        ("PYTHON_JULIACALL_OPTLEVEL", "3"),
    ):
        os.environ[k] = os.environ.get(k, default)

# Actual start of module - now that juliacall can be imported
from juliacall import Main as jl, convert as jlconvert
import numpy as np

# Load the main package + linear solver
jl.seval("using JutulDarcy, Jutul, HYPRE, GeoEnergyIO")

def test_file_path(*args):
    """
    Get the path to a test file in the GeoEnergyIO package. This may trigger a
    download if it is the first time the given example file is requested. If a
    path is returned, the file is available on-disk at that location.

    Examples:
    test_file_path("SPE1", "SPE1.DATA")
    test_file_path("SPE9", "SPE9.DATA")
    test_file_path("OLYMPUS_1", "OLYMPUS_1.DATA")
    test_file_path("NORNE_NOHYST", "NORNE_NOHYST.DATA")
    test_file_path("EGG", "EGG.DATA")

    """
    return jl.GeoEnergyIO.test_input_file_path(*args)

def simulate_data_file(data_file_name, convert = True, units = jl.missing, **kwargs):
    """
    Simulate a reservoir .DATA file using JutulDarcy and return the results as a
    Python dictionary. The resulting dictionary has the following fields:

    - WELLS: A dictionary of well results, where each key is a well name and the
      value is a dictionary of results for that well.
    - FIELD: A dictionary of field results.
    - DAYS: A numpy array of time in days.
    - STATES: A list of dictionaries, each representing the state of the reservoir
      at a given time step. The field vary based on the type of simulation.
    
    If you are looking for files to test, see test_file_path() for a few
    examples of files to test.

    Examples:
    pth = test_file_path("SPE1", "SPE1.DATA")
    # Simulate the data file and convert to Python dictionary
    res = jd.simulate_data_file(pth, units = "field", restart = True, output_path = "/tmp")
    # Write output to disk and apply restart (restarting if simulation was aborted, otherwise retrieving results from disk)
    import tempfile
    res = jd.simulate_data_file(pth, restart = True, output_path = tempfile.gettempdir())
    # Simulate and change the units to field units even if input file has other units
    res = jd.simulate_data_file(pth, units = "field")

    """
    units = _convert_units(units)
    res = jl.JutulDarcy.simulate_data_file(data_file_name, **kwargs)
    if convert:
        out = convert_to_pydict(res, units=units)
    else:
        out = res
    return out

def convert_to_pydict(result, units = jl.missing):
    c = result.extra[jl.Symbol("case")]
    units = _convert_units(units)
    smry = jl.JutulDarcy.summary_result(c, result, units)

    wdict = dict()
    for k in jl.keys(smry["VALUES"]["WELLS"]):
        wdict[k] = _numdict_to_py(smry["VALUES"]["WELLS"][k])
    fdict = _numdict_to_py(smry["VALUES"]["FIELD"])

    out = dict()
    out["WELLS"] = wdict
    out["FIELD"] = fdict
    day = 24*3600.0
    out["DAYS"] = np.array(np.divide(smry["TIME"].seconds, day))
    pystates = []
    for state in result.states:
        pystates.append(_numdict_to_py(state))
    out["STATES"] = pystates

    return out

def _numdict_to_py(d_jl):
    d_py = dict()
    for k in jl.keys(d_jl):
        d_py[jl.String(k)] = np.array(d_jl[k])
    return d_py

def _convert_units(units):
    if isinstance(units, str):
        if units not in ["field", "si", "metric", "lab"]:
            raise RuntimeError("units must be one of field, si, metric, lab")
        units = jl.Symbol(units)
    return units
