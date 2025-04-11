from juliacall import Main as jl, convert as jlconvert
import numpy as np

# Load the main package + linear solver
jl.seval("using JutulDarcy, Jutul, HYPRE")
def main():
    """Entry point for the application script"""
    print("Call your main application code here!")
