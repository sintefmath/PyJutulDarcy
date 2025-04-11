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
