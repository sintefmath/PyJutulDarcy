from .julia_import import jl
import numpy as np

def convert_to_pydict(result, case = None, units = jl.missing):
    """
    Convert a JutulDarcy result to a Python dictionary.
    The resulting dictionary has the following fields:

    - WELLS: A dictionary of well results, where each key is a well name and the
      value is a dictionary of results for that well.
    - FIELD: A dictionary of field results.
    - DAYS: A numpy array of time in days.
    - STATES: A list of dictionaries, each representing the state of the reservoir
      at a given time step. The field vary based on the type of simulation.
    """
    if case == None:
        case = result.extra[jl.Symbol("case")]
    units = _convert_units(units)
    smry = jl.JutulDarcy.summary_result(case, result, units)

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

def _stringdict_to_symdict(d_py):
    d_jl = jl.Dict()
    for k in d_py.keys():
        ks = jl.Symbol(k)
        d_jl[ks] = d_py[k]
    return d_jl

def symdict_to_pydict(d_jl):
    d_py = dict()
    for k, v in d_jl.items():
        d_py[str(k)] = d_jl[jl.Symbol(k)]
    return d_py
