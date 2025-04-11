from juliacall import Main as jl, convert as jlconvert
import numpy as np

# Load the main package + linear solver
jl.seval("using JutulDarcy, Jutul, HYPRE, GeoEnergyIO")
def main():
    """Entry point for the application script"""
    print("Call your main application code here!")

def test_file_path(*args):
    return jl.GeoEnergyIO.test_input_file_path(*args)

def simulate_data_file(fname, **kwargs):
    return jl.JutulDarcy.simulate_data_file(fname, **kwargs)

