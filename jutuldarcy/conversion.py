from .julia_import import jl
import numpy as np

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
