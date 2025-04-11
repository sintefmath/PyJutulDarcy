from juliacall import Main as jl, convert as jlconvert
import numpy as np

# Load the main package + linear solver
jl.seval("using JutulDarcy, Jutul, HYPRE, GeoEnergyIO")
def main():
    """Entry point for the application script"""
    print("Call your main application code here!")

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
    # Convert wells
    jl.JutulDarcy.reservoir_measurables(model, wellresult, states)
    c = result.extra[jd.jl.Symbol("case")]
    smry = jd.jl.JutulDarcy.summary_result(c, result)
    # Convert field measurables
    # Convert states
    error()
    return 0
