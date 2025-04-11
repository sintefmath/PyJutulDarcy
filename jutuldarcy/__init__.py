from juliacall import Main as jl, convert as jlconvert
import numpy as np

# Load the main package + linear solver
jl.seval("using JutulDarcy, Jutul, HYPRE, GeoEnergyIO")

def test_file_path(*args):
    return jl.GeoEnergyIO.test_input_file_path(*args)

def simulate_data_file(fname, convert = True, **kwargs):
    res = jl.JutulDarcy.simulate_data_file(fname, **kwargs)
    if convert:
        out = convert_to_pydict(res)
    else:
        out = res
    return out

def convert_to_pydict(result):
    c = result.extra[jl.Symbol("case")]
    smry = jl.JutulDarcy.summary_result(c, result)

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
